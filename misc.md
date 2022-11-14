---
title: Miscellaneous Tips
created: 2021-12-14
updated: 2022-11-14
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

## Why some YAML files start with 3 dashs (`---`)?

The three dashes `---` are used to signal the start of a document

1. To signal the document start `after directives`, i.e., `%YAML` or `%TAG`
   lines according to the current spec. For example:

```yaml
%YAML 1.2
%TAG !foo! !foo-types/
---
myKey: myValue
```

2. To signal the document start when you have **multiple yaml documents in the
   same stream**, e.g., a yaml file:

```yaml
doc 1
---
doc 2
```

If doc 2 has some preceding directives, then we have to use three dots `...` to
indicate the end of doc 1 (and the start of potential directives preceding
doc 2) to the parser. For example:

```yaml
doc 1
...
%TAG !bar! !bar-types/
---
doc 2
```

3. An **explicit** document begins with an explicit directives end marker line
   but no directives. (ref 4)

Refs:

1. [why --- (3 dashes/hyphen) in yaml file?](https://stackoverflow.com/questions/50788277/why-3-dashes-hyphen-in-yaml-file)
2. [Brief YAML reference](https://camel.readthedocs.io/en/latest/yamlref.html)
3. [YAML specification v1.2.2 - 6.8. Directives](https://yaml.org/spec/1.2.2/#68-directives)
4. [YAML specification v1.2.2 - 9.1.4. Explicit Documents](https://yaml.org/spec/1.2.2/#914-explicit-documents)
