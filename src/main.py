from langchain_unstructured import UnstructuredLoader

file_path = ["./assets/CG101_CG102_CG103.pdf"]

loader = UnstructuredLoader(file_path)

docs = loader.load()

print(docs[0])

if __name__ == '__main__':
     unittest.main()