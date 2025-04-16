# GinsFSM

```{note}

    This project is finalized.

    I'm re-writing the idea of ginsfsm in C language.

```

## The name of the new project is [`Yuneta Simplified`](https://github.com/artgins/yunetas).

## Key Concepts

Can you **draw your development**?

Can you **view the behavior of your application in real time**?

With this framework, **you can**!

GinsFSM is a Python library for developing systems based on [finite-state machines](http://en.wikipedia.org/wiki/Finite-state_machine).
This model is especially useful for building networking and communication applications.

- All objects, called **gobjs**, are instances of a class derived from `ginsfsm.gobj.GObj`.
- Each `GObj` has an internal **simple-machine** that defines its behavior.
- Communication between `gobjs` happens through **events**.

As a result, the system is **fully asynchronous and event-driven**.

All objects share a simple and consistent interface — just change the event name and the data payload.

## Features

- Fully asynchronous HTTP server  
- WSGI server  
- WinSocket server/client compatible with [`sockjs`](https://github.com/sockjs/sockjs-client)  

You can run **multiple WSGI applications** simultaneously.

## Project Scaffolding

GinsFSM includes a variety of scaffolds to help you generate new projects.

Similar to the [`Pyramid`](http://www.pylonsproject.org/) framework's `pcreate` / `pserve` commands,  
GinsFSM provides `gcreate` / `gserve` commands for creating and running projects.

Using the `gcreate` command with the `multi_pyramid_wsgi` scaffold, you can generate a project with multiple WSGI applications —  
one of which can be a `Pyramid` WSGI application.

`GObj` objects are Pyramid "location-aware" resources, and the object model is a **hierarchical tree** —  
making **traversal dispatching** a natural fit.

## Support and Documentation

- Documentation: [ginsfsm](https://pythonhosted.org/ginsfsm/index.html)  
- Source Code: [GitHub](https://github.com/niyamaka/ginsfsm)

## License

Copyright (c) 2012, Ginés Martínez Sánchez.  
GinsFSM is released under the terms of the [MIT License](http://www.opensource.org/licenses/mit-license)
