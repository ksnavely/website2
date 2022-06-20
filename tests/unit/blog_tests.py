"""
_blog_tests_

Unit tests coverage for website.blog.
"""
import unittest
from unittest import mock

from website import blog


class BlogTests(unittest.TestCase):
    """
    Test the blog create/get/update, singleton.
    """

    @mock.patch("website.blog.MongoClient")
    def client_singleton_test(self, m_mc):
        """
        Make sure we can fetch the mongo client, and that it's a singleton.
        """
        m_mc.return_value = mock.Mock()

        client1 = blog._client()
        client2 = blog._client()
        self.assertEqual(client1, client2)

    @mock.patch("website.blog.arrow.utcnow")
    @mock.patch("website.blog._get_blog_posts_collection")
    def create_post_test(self, m_g_collection, m_utc):
        ack = "ack"
        cursor = mock.Mock()
        cursor.insert_one = mock.Mock(return_value=ack)
        m_g_collection.return_value = cursor

        timestamp = "12 some json timestamp"
        utc = mock.Mock()
        utc.for_json = mock.Mock(return_value=timestamp)
        type(utc).timestamp = timestamp
        m_utc.return_value = utc

        tags = ["dags"]
        post = {
            "title": "title",
            "author": "author",
            "text": "text",
            "date": timestamp,
            "tags": tags,
        }

        ret = blog.create_post(post["title"], post["author"], post["text"], tags=tags)

        cursor.insert_one.assert_called_once_with(post)

    @mock.patch("website.blog._get_blog_posts_collection")
    def get_posts_test(self, m_g_collection):
        """
        Test the get_posts functionality and ensure the results
        are reverse date sorted.
        """
        posts = [{"date": 1}, {"date": 2}]
        cursor = mock.Mock()
        cursor.find = mock.Mock(return_value=posts)
        m_g_collection.return_value = cursor

        ret_posts = blog.get_posts()

        # Verify reverse date sort
        self.assertEqual([posts[1], posts[0]], ret_posts)

        cursor.find.assert_called_once_with()

    @mock.patch("website.blog._get_blog_posts_collection")
    def get_posts_count_test(self, m_g_collection):
        """
        Test the get_posts functionality with count.
        """
        posts = [{"date": 1}, {"date": 2}]
        cursor = mock.Mock()
        cursor.find = mock.Mock(return_value=posts)
        m_g_collection.return_value = cursor

        ret_posts = blog.get_posts(count=1)

        # Verify reverse date sort
        self.assertEqual([posts[1]], ret_posts)

        cursor.find.assert_called_once_with()

    @mock.patch("website.blog._get_blog_posts_collection")
    def get_posts_skip_test(self, m_g_collection):
        """
        Test the get_posts functionality with skip.
        """
        posts = [{"date": 1}, {"date": 2}]
        cursor = mock.Mock()
        cursor.find = mock.Mock(return_value=posts)
        m_g_collection.return_value = cursor

        ret_posts = blog.get_posts(skip=1)

        # Verify reverse date sort
        self.assertEqual([posts[0]], ret_posts)

        cursor.find.assert_called_once_with()

    @mock.patch("website.blog._get_blog_posts_collection")
    def get_posts_count_skip_test(self, m_g_collection):
        """
        Test the get_posts functionality with count and skip.
        """
        posts = [{"date": 1}, {"date": 2}, {"date": 3}]
        cursor = mock.Mock()
        cursor.find = mock.Mock(return_value=posts)
        m_g_collection.return_value = cursor

        ret_posts = blog.get_posts(count=1, skip=1)

        # Verify reverse date sort
        self.assertEqual([posts[1]], ret_posts)

        cursor.find.assert_called_once_with()

    @mock.patch("website.blog._get_blog_posts_collection")
    def get_posts_by_date_test(self, m_g_collection):
        """
        Test the by-date functionality for get_posts.
        """
        date = 42
        posts = [{"date": 1}, {"date": 2}]
        cursor = mock.Mock()
        cursor.find = mock.Mock(return_value=posts)
        m_g_collection.return_value = cursor

        ret_posts = blog.get_posts(date=date)

        # Verify reverse date sort
        self.assertEqual([posts[1], posts[0]], ret_posts)

        cursor.find.assert_called_once_with({"date": {"$regex": date}})

    @mock.patch("website.blog.ObjectId")
    @mock.patch("website.blog._get_blog_posts_collection")
    def get_post_test(self, m_g_collection, m_obj):
        obj_id = "object id 17"
        m_obj.return_value = obj_id

        post = {"data": "data"}
        cursor = mock.Mock()
        cursor.find_one = mock.Mock(return_value=post)
        m_g_collection.return_value = cursor

        post_id = 17

        ret_post = blog.get_post(post_id)

        self.assertEqual(post, ret_post)

        cursor.find_one.assert_called_once_with({"_id": obj_id})
        m_obj.assert_called_once_with(post_id)

    @mock.patch("website.blog.ObjectId")
    @mock.patch("website.blog._get_blog_posts_collection")
    def update_post_test(self, m_g_collection, m_obj):
        ack = "ack"
        cursor = mock.Mock()
        cursor.update_one = mock.Mock(return_value=ack)
        m_g_collection.return_value = cursor

        obj_id = "object id 12"
        m_obj.return_value = obj_id

        post_id = 12
        post = {
            "title": "title",
            "author": "author",
            "text": "text",
            "date": "json date",
            "tags": ["a", "b"],
        }

        ret = blog.update_post(
            post_id,
            post["title"],
            post["author"],
            post["text"],
            post["date"],
            post["tags"],
        )

        cursor.update_one.assert_called_once_with({"_id": obj_id}, {"$set": post})
        m_obj.assert_called_once_with(post_id)
        self.assertEqual(ack, ret)
