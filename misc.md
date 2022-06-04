---
title: Miscellaneous Tips
updated: 2021-12-14
created: 2022-06-04
tags:
  - general
---

## VSCode: How to execute multiple commands in one shortcut with tasks

While writing codes, we usually want do multiple consequenced commands (like a
pipe: `fix` -> `sort` -> `format` -> `save`), and wouldn't even better to
combine them in to one shortcut key. Here is how could you customize your
actions **without extra extension**:

Firstly, define your tasks (example for `tasks.json`):

```jsonc
{
  // See https://go.microsoft.com/fwlink/?LinkId=733558
  // for the documentation about the tasks.json format
  "version": "2.0.0",
  "tasks": [
    {
      "label": "sort",
      "command": "${command:editor.action.organizeImports}"
    },
    {
      "label": "format",
      "command": "${command:editor.action.formatDocument}"
    },
    {
      "label": "save",
      "command": "${command:workbench.action.files.save}"
    },
    {
      "label": "fast-format",
      "dependsOrder": "sequence",
      "dependsOn": ["sort", "format", "save"]
    }
  ]
}
```

Then, define key map in `keybindings.json`:

```jsonc
[
  {
    "key": "F4",
    "command": "workbench.action.tasks.runTask",
    "args": "fast-format"
  }
]
```

Finally, try to press `F4` to test whether it execute your tasks correctly.

Another extra useful setup:

```jsonc
{
  // If the Tasks: Run Task command is slow,
  // disabling auto detect for task providers may help.
  "task.autoDetect": "off"
}
```

Put `tasks.json` to same location with `settings.json` or in workspace level
`.vscode` directory.

References:

1. [VS Code: bind one key to multiple commands without an extension](https://dae.me/blog/2603/vs-code-bind-one-key-to-multiple-commands-without-an-extension/)
2. [ Integrate with External Tools via Tasks: Task auto-detection](https://code.visualstudio.com/docs/editor/tasks#_task-autodetection)
