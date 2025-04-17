INGInious
=========

.. image:: https://api.codacy.com/project/badge/Grade/7cd8340004ef4d409143d5c24259efc1
   :alt: Codacy Badge
   :target: https://app.codacy.com/gh/INGInious/INGInious?utm_source=github.com&utm_medium=referral&utm_content=INGInious/INGInious&utm_campaign=Badge_Grade_Dashboard
.. image:: https://app.codacy.com/project/badge/Coverage/9102bbf54901478dbe288a386195f77e
   :alt: Codacy coverage Badge
   :target: https://www.codacy.com/gh/INGInious/INGInious/dashboard?utm_source=github.com&utm_medium=referral&utm_content=INGInious/INGInious&utm_campaign=Badge_Coverage
.. image:: https://github.com/INGInious/INGInious/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/INGInious/INGInious/actions
.. image:: https://github.com/INGInious/INGInious/actions/workflows/env_containers.yml/badge.svg
    :target: https://github.com/INGInious/INGInious/actions
.. image:: https://readthedocs.org/projects/inginious/badge/?version=latest
    :target: https://readthedocs.org/projects/inginious/?badge=latest
.. image:: https://weblate.info.ucl.ac.be/widgets/inginious/-/frontend/svg-badge.svg
    :target: https://weblate.info.ucl.ac.be/engage/inginious/?utm_source=widget

INGInious is an intelligent grader that allows secured and automated testing of code made by students.

It is written in Python and uses Docker_ to run student's code inside a secured environment.

INGInious provides a backend which manages interaction with Docker and grade code, and a frontend which allows students to submit their code in a simple and beautiful interface. The frontend also includes a simple administration interface that allows teachers to check the progression of their students and to modify exercices in a simple way.

The backend is independent of the frontend and was made to be used as a library.

INGInious can be used as an external grader for EDX. The course `Paradigms of Computer Programming - Fundamentals`_ uses INGInious to correct students' code.

.. _Docker: https://www.docker.com/
.. _Paradigms of Computer Programming - Fundamentals: https://www.edx.org/course/louvainx/louvainx-louv1-1x-paradigms-computer-2751

How to install?
---------------

Simply run:

.. code-block::

   $ docker compose up --build

> Note that you can override the registry and containers version by setting the `REGISTRY` and
> `VERSION` environment variables.

And access http://localhost:9000 in your browser.

*The default login and password are* ``superadmin``.

The ``--build`` argument is optional, use it if you want to rebuild locally the core containers.
If you want to simply pull them from the project's registry, this argument is not required.

Docker-compose will create a ``tasks`` folder if it does not exist already.

You can then add new courses to your fresh INGInious instance by installing them in the ``tasks`` folder.

For example, the INGInious tutorial course is installed with the following commands:

.. code-block::

   $ git clone https://github.com/INGInious/demo-tasks.git
   $ mv demo-tasks/tutorial tasks/

*If you encounter permission errors, you should run the following command:*

.. code-block::

   $ sudo chown -R <your_user>:<your_user_group> tasks

*This can happen when the tasks directory is created by docker-compose.*

Note that the `configuration.deploy.yaml` file provided is a sample configuration, the secret key **must** be changed by administrators in production deployments.

.. _Manual installation: https://docs.inginious.org/en/latest/admin_doc/install_doc/installation.html

`Manual installation`_ is also possible with pip.

Documentation
-------------

The documentation is available on Read the Docs:

- For the stable branch : http://inginious.readthedocs.org/
- For the master (dev) branch (not always up to date) : http://inginious.readthedocs.org/en/latest/index.html

On Linux, run ``make html`` in the directory ``/doc`` to create a html version of the documentation.

Roadmap
-------

INGInious is continuously improved. The various Work In Progress tasks are described in the Roadmap_ of the project.
 
 .. _Roadmap: https://github.com/UCL-INGI/INGInious/wiki/Roadmap
 
Notes on security
-----------------

Docker containers can be used securely with SELinux enabled. Please do not run untrusted code without activating SELinux.

Mailing list
------------

A mailing list for both usage and development discussion can be joined by registering here_.

..  _here: https://sympa-2.sipr.ucl.ac.be/sympa/info/inginious
