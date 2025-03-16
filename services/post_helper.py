from fastapi import HTTPException
from sqlalchemy import select
from db.db_post_table import db_posts_table
from db.db_comment_table import db_comments_table
from db.db_likes_table import db_likes_table
from db.db_user_table import db_user_table
from models.post_model import PostIn, PostOut
from models.user_model import UserQueryOut
from database_connect import dbs
from sqlalchemy.orm import aliased


class PostHelper:

    @staticmethod
    async def get_posts(post_id: int = None, user_id: int = None, limit: int = 10, offset: int = 0):
        posts_alias = aliased(db_posts_table, name="posts")
        user_alias = aliased(db_user_table, name="user")
        likes_alias = aliased(db_likes_table, name="likes")
        comment_alias = aliased(db_comments_table, name="comments")

        # Base query
        query = (
            select(posts_alias, user_alias, likes_alias, comment_alias)
            .join(user_alias, posts_alias.c.user_id == user_alias.c.id)
            .outerjoin(comment_alias, posts_alias.c.post_id_table == comment_alias.c.post_comment_id)
            .outerjoin(likes_alias, posts_alias.c.post_id_table == likes_alias.c.post_like_id)
        )

        # If post_id is specified, filter for that post
        if user_id:
            query = query.where(posts_alias.c.user_id == user_id)
        elif post_id:
            query = query.where(posts_alias.c.post_id_table == post_id)
        else:
            query = query.limit(limit)  # Apply limit only when fetching multiple posts
        query = query.offset(offset)  # Apply offset only when fetching multiple posts
        try:
            posts = await dbs.fetch_all(query)  # Fetch all rows related to this post or multiple posts
            if not posts:
                raise HTTPException(status_code=404, detail="Post(s) not found")

            organized_posts = []
            post_map = {}  # Dictionary to track posts by ID

            for post in posts:
                post = dict(post)  # Convert record to dictionary

                post_id_key = post["post_id_table"]

                # If post not in map, initialize it
                if post_id_key not in post_map:
                    post_copy = post.copy()
                    organized_post = {
                        k: post_copy.pop(k)
                        for k in post.keys()
                        if not any([k.endswith("_id"), k.endswith("_like"), k.endswith("_comment")])
                    }

                    # Extract user details
                    users = {
                        k: organized_post.pop(k)
                        for k in UserQueryOut.schema()["properties"].keys()
                        if k in organized_post
                    }
                    organized_post["user"] = users
                    organized_post.pop("password", None)  # Remove sensitive data
                    organized_post["likes"] = []  # Initialize empty likes list
                    organized_post["comments"] = []  # Initialize empty comments list

                    post_map[post_id_key] = organized_post

                # Extract likes if present
                if post.get("likes_id_table"):
                    like_data = {
                        "likes_id": post["likes_id_table"],
                        "user_id": post["user_like_id"],
                        "created_at": post["likes_created_at"]
                    }
                    if like_data not in post_map[post_id_key]["likes"]:
                        post_map[post_id_key]["likes"].append(like_data)

                # Extract comments if present
                if post.get("comment_id_table"):
                    comment_data = {
                        "comment_id": post["comment_id_table"],
                        "user_id": post["user_comment_id"],
                        "text": post["comment_text"],
                        "created_at": post["comment_created_at"],
                        "updated_at": post["comment_updated_at"]
                    }
                    if comment_data not in post_map[post_id_key]["comments"]:
                        post_map[post_id_key]["comments"].append(comment_data)

            organized_posts = list(post_map.values())  # Convert dictionary values to a list

            return organized_posts if not post_id else organized_posts[0]

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))



    @staticmethod
    async def create_post(post_data: PostIn):
        query = db_posts_table.insert().values(post_data.model_dump())
        post_id = await dbs.execute(query)
        post = await PostHelper.get_posts(post_id)
        return post
    
    @staticmethod
    async def delete_post(post_id: int, user_id: int):
        query_post = db_posts_table.select().where(db_posts_table.c.post_id_table == post_id)
        post = await dbs.fetch_one(query_post)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        if post['user_id'] != user_id:
            raise HTTPException(status_code=401, detail="Unauthorized access")
        query = db_posts_table.delete().where(db_posts_table.c.post_id_table == post_id)
        return await dbs.execute(query)
