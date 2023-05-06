"""
wonka: runtime class and object creation, made simple
Corey Rayburn Yung <coreyrayburnyung@gmail.com>
Copyright 2023, Corey Rayburn Yung
License: Apache-2.0

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    
ToDo:
    Increase test coverage

 
For Contributors and Developers:

As with all of my packages, I use Google-style docstrings and follow the Google 
Python Style Guide (https://google.github.io/styleguide/pyguide.html) with two 
notable exceptions:
    1) I always add spaces around "=". This is because I find it more readable 
        and it is practically the norm with type annotations adding the spaces
        to function and method signatures. I realize that this will seem alien
        to many coders, but it is far easier on my eyes.
    2) I use some so-called "power features", primarily dunder methods, to make
        my interfaces easier to access and use. This is disfavored in the Google
        Python Style Guide because such code is often more difficult for others
        to read. To address that concern, I try to document and comment as to
        what the code is doing whenever I used any of the "power features" of
        Python.

My packages lean heavily toward over-documentation and verbosity. I do this to
make them more accessible to beginnning coders and generally more usable. The 
one exception to that general rule is unit tests, which hopefully are clear 
enough to not require further explanation. If there is any area of the 
documentation or code that could be made clearer, please don't hesitate to email 
me orany other package maintainer - I want to ensure this package is as 
accessible and useful as possible.
     
"""
__version__ = '0.1.0'

__package__ = 'wonka'

__author__ = 'Corey Rayburn Yung'


from .base import *
from .configuration import *
from .dispatchers import *
from .managers import *
from .producers import *
from .prototypers import *
from .registries import *
from .shared import *
from .storage import *