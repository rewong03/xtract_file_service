import docker
import os
import uuid
import multiprocessing as mp
from celery.exceptions import SoftTimeLimitExceeded

client = docker.from_env()
extractor_names = ['tabular', 'jsonxml', 'netcdf', 'keyword', 'image', 'maps', 'matio']


def build_image(extractor):
    """Helper function for building multiple images using multiprocessing.

    Parameter:
    extractor (str): Name of the extractor image to build (one of the items from the extractor_names list).
    """
    client.images.build(path=os.path.join('app/dockerfiles', extractor), tag="xtract-" + extractor)
    return "Done building xtract-{}".format(extractor)


def build_all_images(multiprocess=False):
    """Builds all extractor images from the extractor_names list.

    Parameter:
    multiprocess (bool): Whether to build the images in parallel or not. Not entirely sure if this works.
    """
    for extractor in extractor_names:
        try:
            client.images.remove("xtract-" + extractor, force=True)
        except:
            pass
        client.images.prune()
    print("Done deleting")
    if multiprocess is False:
        for extractor in extractor_names:
            print(os.path.join('app/dockerfiles', extractor))
            client.images.build(path=os.path.join('app/dockerfiles', extractor), tag="xtract-" + extractor)
    else:
        pools = mp.Pool(processes=mp.cpu_count())
        for image in pools.imap_unordered(build_image, extractor_names):
            print(image)

        pools.close()
        pools.join()
    print("Done building")


def extract_metadata(extractor, file_path, cli_args=[]):
    """Extracts metadata from a file using only a single extractor.

        extractor (str): Extractor name from extractor_names list.
        file_path (str): File path of file to extract metadata from.
        cli_args (list): Additional command line arguments to pass to the extractor
        in a list format (e.g. ["--text_string", "string to pass"]).

        Returns:
        (str): String version of dictionary containing metadata.
        """
    if extractor in extractor_names:
        directory = os.path.abspath(file_path)
        filename = os.path.basename(file_path)
        cli_command = ["--path", directory]

        if extractor == "image":
            cli_command = ["--image_path", directory, "--mode", "predict"]
        cli_command.extend(cli_args)

        # Containers don't get removed when task is resubmitted, so we need a way to identify the container
        container_id = str(uuid.uuid4())
        try:
            metadata = client.containers.run("xtract-" + extractor, cli_command, auto_remove=False,
                                             volumes={directory: {"bind": directory}},
                                             name=container_id).decode('utf-8')

            return metadata
        except SoftTimeLimitExceeded:
            client.containers.get(container_id).remove(v=True, force=True)
            raise SoftTimeLimitExceeded
        except:
            return "The {} extractor failed to extract metadata from {}".format(extractor, filename)
    else:
        return "Not an extractor"





