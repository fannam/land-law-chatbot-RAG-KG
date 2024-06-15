from gpt4all import Embed4All
text = 'The quick brown fox jumps over the lazy dog'
embedder = Embed4All(device='gpu')
output = embedder.embed(text)
print(output)