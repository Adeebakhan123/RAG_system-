from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, PyMuPDFLoader

def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()

def load_directory(folder_path):
    loader = DirectoryLoader(
        folder_path,
        glob="**/*.pdf",
        loader_cls=PyMuPDFLoader
    )
    return loader.load()