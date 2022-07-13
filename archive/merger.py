import argparse # See https://docs.python.org/3/library/argparse.html
from bs4 import BeautifulSoup # See https://www.crummy.com/software/BeautifulSoup/bs4/doc/

# CLI arguments parsing
parser = argparse.ArgumentParser(description = 'Merge two or more Twine 2 stories.')

parser.add_argument(
    "-s", "--story",
    dest = "story_ifid",
    help = "Story ID ('ifid' attribute of <tw-storydata>)",
    required = True
)
parser.add_argument(
    "-o", "--output",
    dest = "output_filename",
    help = "Output filename (Twine 2 archive)",
    required = True
)
parser.add_argument(
    "-i", "--input",
    dest = "input_filenames",
    nargs = "+",
    help = "Input filenames (Twine 2 archives, one or more)",
    required = True
)

args = parser.parse_args()
# End CLI arguments parsing

# Global objects initialization
story_attributes = {}
story_style = None
story_script = None
story_passages = {}
# End global objects initialization

# Loop on input files (twine archives)
for filename in args.input_filenames:

    # Open input file (twine archive)
    with open(filename, "r") as f:

        # HTML parsing of input file
        soup = BeautifulSoup(f, 'html.parser')

        # Loop on stories
        for story in soup.find_all("tw-storydata"):
            # Ignore all stories without the provided id
            if story.get("ifid") == args.story_ifid:
                # Store story attributes of the first archive
                if not story_attributes:
                    story_attributes = story.attrs
                # Store story css style of the first archive
                if not story_style:
                    story_style = story.find("style")
                # Store story js script of the first archive
                if not story_script:
                    story_script = story.find("script")
                # Loop on story passages
                for passage in story.find_all("tw-passagedata"):
                    # Passage name is the unique identifier of passage
                    passage_name = passage.get("name")
                    # Overwriting is allowed only if previous passage was empty
                    if passage_name not in story_passages or not story_passages[passage_name].get_text():
                        story_passages[passage_name] = passage
# End loop on input files
# Now story_passages containes all passages from all stories

# Output story initialization
soup = BeautifulSoup("<tw-storydata></tw-storydata>", 'html.parser')
story = soup.find("tw-storydata")

# Set story attributes, style and script
story.attrs = story_attributes
story.append(story_style)
story.append(story_script)

# Loop on story passages
# Values of story_passages dictionary are sorted by pid, an integer
for index, value in enumerate(
    sorted(
        story_passages.items(),
        key = lambda item: int(item[1].get("pid"))
    )
):
    passage_name, passage = value
    # Passage pids in a story can't be duplicated, so reassign them in order
    passage["pid"] = index + 1
    # Add new passage to output story
    story.append(passage)

# Write Twine 2 archive to output filename
with open(args.output_filename, "w") as f:
    f.write(soup.prettify())
