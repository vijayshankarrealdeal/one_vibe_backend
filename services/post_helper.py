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
    async def get_posts(post_id: int = None):
        posts_alias = aliased(db_posts_table, name="posts")
        user_alias = aliased(db_user_table, name="user")
        likes_alias = aliased(db_likes_table, name="likes")
        comment_alias = aliased(db_comments_table, name="comments")
        if post_id:
            query = (
                select(posts_alias, user_alias, likes_alias, comment_alias)
                .join(user_alias, posts_alias.c.user_id == user_alias.c.id)
                .outerjoin(comment_alias, posts_alias.c.post_id_table == comment_alias.c.post_comment_id)
                .outerjoin(likes_alias, posts_alias.c.post_id_table == likes_alias.c.post_like_id)
                .where(posts_alias.c.post_id_table == post_id)
            )
        else:
            query = (
                select(posts_alias, user_alias, likes_alias, comment_alias)
                .join(user_alias, posts_alias.c.user_id == user_alias.c.id)
                .outerjoin(comment_alias, posts_alias.c.post_id_table == comment_alias.c.post_comment_id)
                .outerjoin(likes_alias, posts_alias.c.post_id_table == likes_alias.c.post_like_id)
            )
        try:
            posts = await dbs.fetch_all(query)  # Fetch all rows related to this post
            if not posts:
                raise HTTPException(status_code=404, detail="Post not found")

            organized_post = None
            likes_list = []
            comments_list = []

            for post in posts:
                post = dict(post)  # Convert record to dictionary

                # Initialize post structure only once
                if not organized_post:
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

                # Extract likes if present
                if post.get("likes_id_table"):
                    like_data = {
                        "likes_id": post["likes_id_table"],
                        "user_id": post["user_like_id"],
                        "created_at": post["likes_created_at"]
                    }
                    if like_data not in likes_list:
                        likes_list.append(like_data)

                # Extract comments if present
                if post.get("comment_id_table"):
                    comment_data = {
                        "comment_id": post["comment_id_table"],
                        "user_id": post["user_comment_id"],
                        "text": post["comment_text"],
                        "created_at": post["comment_created_at"],
                        "updated_at": post["comment_updated_at"]
                    }
                    if comment_data not in comments_list:
                        comments_list.append(comment_data)

            # Assign extracted likes and comments to the post
            if organized_post:
                organized_post["likes"] = likes_list
                organized_post["comments"] = comments_list

            return organized_post

        except Exception as e:
            print(f"Error fetching post {post_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")


    @staticmethod
    async def create_post(post_data: PostIn):
        query = db_posts_table.insert().values(post_data.model_dump())
        post_id = await dbs.execute(query)
        post = await PostHelper.get_posts(post_id)
        return post
