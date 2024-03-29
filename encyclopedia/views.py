from django.shortcuts import render
import markdown
from . import util
import random


def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })

    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })


def search(request):
    entry_search = request.POST.get('q')

    if entry_search:
        html_content = convert_md_to_html(entry_search)

        if html_content:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })

        else:
            allEntries = util.list_entries()
            reckon = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    reckon.append(entry)

            if reckon:
                return render(request, "encyclopedia/search.html", {
                    "reckon": reckon
                })

            else:
                return render(request, "encyclopedia/error.html", {
                    "message": "No entries found for '{0}'".format(entry_search)
                })

    # Handle the case where entry_search is None or html_content is None
    return render(request, "encyclopedia/error.html", {
        "message": "Entry not found"
    })


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html", {

        })
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist:
            return render(request, "encyclopedia/error.html", {
                "message": "'{0}' page already exitsts".format(title)
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })


def random_page(request):
    allEntries = util.list_entries()
    random_entry = random.choice(allEntries)
    html_content = convert_md_to_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": html_content
    })


def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })


def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
