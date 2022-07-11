from bs4 import BeautifulSoup

with open("cerveeelliii.html", "r") as f:
    container = BeautifulSoup(f, 'html.parser').find("tw-storydata")
    for passage in container.find_all("tw-passagedata"):
        passage.decompose()

story_id = container.get("ifid")

passages = {}

filenames = [
    "cerveeelliii-lisa.html",
    "cerveeelliii-enrico.html",
    "cerveeelliii-alessio.html"
]

for filename in filenames:

    with open(filename, "r") as f:

        soup = BeautifulSoup(f, 'html.parser')

        for story in soup.find_all("tw-storydata"):
            if story.get("ifid") == story_id:
                break

        for passage in story.find_all("tw-passagedata"):
            passage_name = passage.get("name")
            if passage_name not in passages and passage.get_text():
                passages[passage_name] = passage

for index, value in enumerate(sorted(passages.items(), key=lambda item: int(item[1].get("pid")))):
    passage_name, passage = value
    passage["pid"] = index + 1
    container.append(passage)

with open("cerveeelliii.html", "w") as f:
    f.write(container.prettify())
