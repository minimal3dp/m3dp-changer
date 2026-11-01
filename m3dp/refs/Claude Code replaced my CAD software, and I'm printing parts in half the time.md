---
title: "Claude Code replaced my CAD software, and I'm printing parts in half the time"
source: "https://www.makeuseof.com/claude-code-replaced-cad-software-printing-parts-half-time/"
published: 2026-08-05
created: 2026-08-05
description: "CAD is starting to understand English."
tags:
  - "clippings"
author:
  - "Yadullah Abidi"
---
[I've been using Claude to design 3D parts](https://www.makeuseof.com/taught-claude-3d-design-prints-real-parts/) for a while now. I first taught it Blender, and then FreeCAD. It got me to some basic working parts, and I figured that was all it could do. I was wrong.

Turns out, Claude Code can do a lot more, and do it more efficiently. It has just about replaced my CAD software, and now I'm designing and printing parts in half the time.



## Designing parts feels completely different

### Claude Code turns ideas into CAD



Claude Desktop was reasonably good at translating plain English into FreeCAD's Python API calls, using the same MCP server, FreeCAD MCP, that exposes the program's scripting layer to the model. Claude Code, however, brings a terminal-native workflow into the mix, which matters more than you might think.

Instead of a single chat window, I now have a persistent session where Claude can read its own error logs, retry failed operations, and reference project files like a running spec sheet for the part I'm working on. Claude Code also handles the FreeCAD MCP server registration through a simple command rather than editing a JSON config by hand, meaning you can literally ask it to install the FreeCAD MCP server and it'll have you ready to work with FreeCAD files in no time.

The biggest difference is in how Claude Code handles iteration. When a boolean operation fails, or a sketch constraint is redundant, Claude Code doesn't just report the error; it reads the FreeCAD Report View output directly, changes its approach, and re-executes without me babysitting the process. This loop was simply not possible in Claude Desktop, where I would have to paste error messages back manually.



FreeCAD MCP is an open-source Model Context Protocol server that enables AI assistants like Claude to create, modify, and analyze parametric FreeCAD models using natural language.

[See at GitHub](https://github.com/neka-nat/freecad-mcp)

## Some jobs still need real CAD skills

### Complex assemblies aren't fully automatic

![Claude running with FreeCAD in the background connected via MCP server.](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2026/07/claude-running-with-freecad-in-the-background-connected-via-mcp-server.JPG?q=49&fit=crop&w=500&dpr=2)

Claude running with FreeCAD in the background connected via MCP server.



One of the biggest problems I ran into with Claude controlling FreeCAD was that complex, multi-body assemblies sent the AI into repetitive iteration loops where it would keep burning tokens as it kept checking viewport screenshots before even designing anything. That problem hasn't gone away entirely, but it's much smaller now.

Running the MCP server with the **\--only-text-feedback** flag cuts down on the screenshot-heavy verification cycle and lets me check the geometry myself in the FreeCAD window instead of paying tokens for every visual confirmation. Considering I have both Claude Code and FreeCAD windows open side by side anyway, this was a no-brainer. Additionally, forks of the FreeCAD MCP project, including ones from developers like [blwfish](https://github.com/blwfish/freecad-mcp) and [contextform](https://github.com/contextform/freecad-mcp), add dozens of additional tools covering CAM toolpath generation, mesh manipulation, and spatial analysis, which gives Claude more direct ways to verify geometry without relying purely on screenshots.



![Claude code with complex assembly in FreeCAD.](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2026/08/claude-code-with-complex-assembly-in-freecad.jpg?q=49&fit=crop&w=825&dpr=2)

Claude code with complex assembly in FreeCAD.


Regardless, if I'm working on intricate assemblies with dependent constraints across multiple bodies, I still have to step in manually. If I'm designing something with more than three or four interacting parts, like a hinge assembly or a multi-piece enclosure with snap fits, it's better to break the job into smaller conversations covering one body at a time, and assemble them myself in FreeCAD afterwards. This keeps each conversation focused and prevents Claude from losing track of which constraint belongs to which sketch — the main source of frustration in my past attempts.

## The biggest win isn't the modeling

### Iteration became dramatically faster

![Claude Code making M4 screws in FreeCAD.](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2026/08/claude-code-making-m4-screws-in-freecad.jpg?q=49&fit=crop&w=825&dpr=2)

Claude Code making M4 screws in FreeCAD.


Complex parts aside, the real time savings still lie in repetitive tasks. Mounting plates with bolt patterns, symmetric cutouts, brackets with fixed hole spacings, and many other similar projects can simply be described in a sentence, and Claude will have a part ready for you in a couple of attempts at most.

My old trick of sketching a rough 2D sketch on paper, photographing it, and handing that image to Claude Code as a starting reference works better. Skadis pegboard hooks, one of my most added features to a 3D print, now get added automatically in a single follow-up prompt, and Claude automatically accounts for existing geometry instead of me manually offsetting sketches.

## It's impressive, but not finished

### A few rough edges still remain

Anything that you'll find hard to describe in natural language is still challenging to work with in Claude Code. Things like close tolerance relationships and GD&T annotations are still hard to specify.


I'd also like better support for saving reusable skills, or macros that Claude can recall across sessions instead of re-deriving the same bolt pattern logic every time. Multi-instance support, where Claude tracks several open FreeCAD documents at once, is starting to come up in some of the newer forks and would make life a lot easier when designing companion parts that need to fit together.

## This is where AI belongs in CAD

### Makers benefit more than anyone else

For the kind of parts most 3D printing hobbyists need, like brackets, mounts, adapters, and enclosures, Claude Code will move this workflow from a neat experiment to something you'll use every day. This also remains one of the best, most hands-on ways to learn CAD software as you design real-world parts instead of following tutorials. It's one of the ways [Claude Code can become your most-used tool, even if you don't code at all](https://www.makeuseof.com/i-dont-code-at-all-but-claude-code-became-my-most-used-tool/).


But once again, Claude doesn't replace CAD knowledge, and sometimes it's faster for me to intervene or just design a sketch instead of describing it. What it does is remove the tedious constraint-wrangling that used to be the biggest time sink in my designing and eventually printing pipeline, and that alone makes it an invaluable tool.

