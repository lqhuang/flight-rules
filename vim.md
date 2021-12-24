---
title: Vim Tips
---

## save with root permission

    :w !sudo tee %
    :w !sudo tee > /dev/null %

References:

1. [How does the vim "write with sudo" trick work?](https://stackoverflow.com/questions/2600783/how-does-the-vim-write-with-sudo-trick-work)
