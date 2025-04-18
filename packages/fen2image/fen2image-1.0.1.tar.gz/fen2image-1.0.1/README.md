# fen2image

Transform a FEN string to a PIL Image.  
A short package for chess players :)
When provided a FEN position as a string, this module will verify the FEN integrity. The verification is quite extensive but I have might have forget some cases.
If the FEN is not correct, an error will be raised.

Usage:

```python
from fen2image import fen2image

img = fen2image('your_fen')
img.show()  # as for every PIL Image
```

Enjoy.
