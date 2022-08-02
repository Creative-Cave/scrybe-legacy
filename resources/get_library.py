from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

auth = os.environ["gist_token"]
library_link = "https://api.github.com/gists/de4f6f7328c06e1d6d33201a64778288"


def get_library() -> dict:
    gist = requests.get(library_link, headers={
                        "Authorization": f"token {auth}"}).json()
    content = gist["files"]["library.json"]["content"]
    return json.loads(content)


def add_review(book, review) -> dict:
    content = get_library()
    current_tick = content["data"]["review_ticker"]
    content["library"][book]["reviews"][current_tick] = {
        "rating": float(review["rating"]),
        "content": review["content"],
        "author": review["author"]
    }

    content["data"]["review_ticker"] += 1

    r = requests.patch(library_link, json={"files": {"library.json": {"content": json.dumps(
        content, indent=4)}}}, headers={"Authorization": f"token {auth}"})
    return r.json()


def add_book(title: str, author: str, url: str) -> dict:
    content = get_library()
    current_tick = content["data"]["id_ticker"]

    title = f"{title[:76]}..." if len(title) > 80 else title

    content["library"][str(current_tick)] = {
        "title": title,
        "author": author,
        "link": url,
        "reviews": {}
    }

    content["data"]["id_ticker"] += 1

    r = requests.patch(library_link, json={"files": {"library.json": {"content": json.dumps(
        content, indent=4)}}}, headers={"Authorization": f"token {auth}"})
    return r.json()


def add_submission(title: str, author: str, url: str) -> dict:
    content = get_library()
    current_tick = content["data"]["submission_ticker"]

    content["submissions"][str(current_tick)] = {
        "title": title,
        "author": author,
        "link": url
    }

    content["data"]["submissions_ticker"] += 1

    r = requests.patch(library_link, json={"files": {"library.json": {"content": json.dumps(
        content, indent=4)}}}, headers={"Authorization": f"token {auth}"})
    return r.json()


def approve_submission(id):
    content = get_library()
    current_tick = content["data"]["id_ticker"]

    submission_details = content["submissions"].pop(str(id))
    content["library"][str(current_tick)] = {
        "title": submission_details["title"],
        "author": submission_details["author"],
        "link": submission_details["link"]
    }

    r = requests.patch(library_link, json={"files": {"library.json": {"content": json.dumps(
        content, indent=4)}}}, headers={"Authorization": f"token {auth}"})
    return r.json()


def decline_submission(id):
    content = get_library()
    del content["submissions"][str(id)]

    r = requests.patch(library_link, json={"files": {"library.json": {"content": json.dumps(
        content, indent=4)}}}, headers={"Authorization": f"token {auth}"})
    return r.json()


def remove_book(id):
    content = get_library()

    del content["library"][str(id)]
    r = requests.patch(library_link, json={"files": {"library.json": {"content": json.dumps(
        content, indent=4)}}}, headers={"Authorization": f"token {auth}"})
    return r.json()
