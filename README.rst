=====
Spoke
=====

Spoke provides a framework for building reusable front-end components.

Installing
==========

The spoke project lives on github_, and is available via pip_.

.. _github: https://github.com/axialmarket/spoke
.. _pip: https://pypi.python.org/pypi?:action=display&name=spoke

Installing v0.1 From Pip
------------------------

::

    sudo pip install spoke==0.1

Installing v0.1 From Source
---------------------------

::

    curl https://github.com/axialmarket/spoke/archive/version_0.1.tar.gz | tar vzxf -
    cd spoke
    sudo python setup.py install


What is a Spoke?
================

A spoke is an executable javascript file that can contain javascript, CSS and HTML templates. In addition, a spoke can have dependencies on other spokes, which allows us to partition front-end components into small discrete chunks and at build time create a single loadable javascript file for a page that includes just the functionality we need. Now, you may be wondering how we embed CSS and HTML templates into an executable javascript file. We're using a somewhat unsophisticated approach; we URI-encode the CSS or HTML content into a string and embed it in some simple javascript that decodes the content and dynamically adds it to the DOM.

A simple example
================

Let's create a spoke for rendering a user's name. This perhaps sounds like it's too simple a task, but there could be some complexity to the logic required:

- To save space, if the user's full name would be more than 20 characters, we will render just their first initial followed by their last name.
- If the user is an internal user, we want to annotate their name with (internal).
- If the user is an internal user masquerading as a regular user, we want to annotate their name with (masq).

For this example, we will use a Backbone model and view, and an Underscore template, but these are implementation choices and not imposed on us just because we are creating a spoke.

Here is the Backbone model we will use:

::

    var UsernameModel = Backbone.Model.extend({
        defaults: { first_name: "",
         last_name: "",
         is_internal: false,
                        is_masq: false }
    });

The view is pretty straightforward:

::

    var UsernameView = Backbone.View.extend({
        className: 'username',
        render: function() {
            this.$el.html(this.template(this.model.attributes));
            return this;
        },
        template: _.template($('#username-template').html())
    });


We will store the Underscore template in a <script> tag with type "text/template":

::

    <script id="username-template" type="text/template">
        <% if (first_name.length + last_name.length >= 20) { %>
            <%= first_name.substr(0,1) %>.
        <% } else { %>
            <%= first_name %>
        <% } >
        <%= last_name %>
        <% if (is_internal) { %>(internal)<% } %>
    <% else if (is_masq) { %>(masq)<% } %> 
    </script>

In addition, we have a CSS file to control the styling of the username:

::

    .username {
        font-size: 18px;
        color: #333;
            white-space: nowrap;
    }

To turn this into a spoke, all we have to do is store these source files in the spoke source tree, which is in /var/spoke/:

::

    js/models/Username.js
    js/views/Username.js
    html/username.html.tpl
    css/username.css

Then we add a definition for this spoke (which we will call, surprise, surprise, "username") to a spoke config, which we add to /etc/spoke/:

::

    # /etc/spoke/username.cfg
    [username]
    js     = [ 'models/Username.js', 'views/Username.js' ]
    html   = 'username.html.tpl'
    css    = 'username.css'
    spokes = 'backbone'

Spokes do not need to have all of these types of files; a spoke might contain only CSS or only javascript content. Note, also, that we have made the "username" spoke dependent on the "backbone" spoke. The definition of the "backbone" spoke in turn references the "underscore" spoke. When we use spokec to generate a spoke, these dependencies are followed and included in the output. As you probably anticipate, if a spoke is referenced multiple times, it only gets included in the output once.

Now that we've defined this spoke, here's how we would call spokec to generate it:

::

    spokec username [add'l spokes] -o path/to/output.js

Each invocation of spokec generates a single executable javascript file containing all of the specified spokes and their dependencies. So typically a service will create a single spoke file for all of its pages, or sometimes a few different spoke files if the pages that service provides are significantly different.

For More Help
=============

::

    spokec --help

License
=======

BSD 3-Clause, see LICENSE.txt_.

.. _LICENSE.txt: https://github.com/axialmarket/spoke/LICENSE.txt

Authors
=======

| Ben Holzman <ben.holzman@axial.net>
| Matthew Story <matt.story@axial.net>
