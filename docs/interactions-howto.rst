Interactions Howto
##########################################

Interactions such as slash commands and buttons are some sexy lil additions to Discord. As such, you'll probably want to use them. Fortunately, VoxelBotUtils makes this pretty easy. Aside from the howto, there's a :ref:`full API reference<interactions>` on the main API reference page.

Responding to an Interaction
------------------------------------------

Interactions need to be responded to, or it shows as "this interaction has failed" in the Discord UI. The Discord API supports a few ways of responding:

* :code:`defer` an interaction, which gives a "processing" message, and respond later.
* :code:`defer_update` an interaction, which doesn't give a processing message, and respond later. This is only available on components.
* :code:`respond` to an interaction, and receive no :class:`discord.Message` object back.

Using the :func:`respond` method will send a type 4 response in the backend, which means that you're unable to receive a message object back from the API, but it does allow you to give responses without showing the loading symbol - a use case for this could be an ephemeral message saying "you can't use this button" or suchlike.

Slash Commands
------------------------------------------

One of the inbuilt cogs in VBU allows you to automatically add all public commands (anything that's not a :func:`meta command<voxelbotutils.checks.meta_command>`, not an :func:`owner only command<discord.ext.commands.is_owner>`, and has its :attr:`add_slash_command<voxelbotutils.Command.add_slash_command>` attribute set to `True` - as is the default) as slash commands.

To [attempt to] add all of your commands as slash commands, run the :code:`!addslashcommands` command in your code, and the bot will attempt to convert all of your arguments and bulk-add the commands to Discord. If this conversion fails, you'll be given a straight traceback of the error instead of anything interpreted, so you can see exactly where the issue stems from.

Most issues stem from using :class:`discord.ext.commands.Greedy`, misordering your optional arguments (they must appear at the end), using even *slightly* complex group commands, and using converters that don't stem from a commonly converted types (though in this instance you can add a :code:`SLASH_COMMAND_ARG_TYPE` attribute being an instance of :class:`voxelbotutils.ApplicationCommandOptionType` to your converter for the bot to use).

When adding arguments to a command, you're able to give descriptions to those arguments using :attr:`voxelbotutils.Command.argument_descriptions`.

Components
------------------------------------------

Components are interactive additions to messages that you're able to send.

All interactions need to be placed into a :class:`MessageComponents` object, and that needs to be populated with :class:`ActionRow`s before finally allowing the components you *actually* want to send.

.. code-block:: python

   components = voxelbotutils.MessageComponents(
      voxelbotutils.ActionRow(
         voxelbotutils.Button("Finally")
      )
   )

Buttons
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using buttons has been made pretty simple. First, you send your button to the user.

.. code-block:: python

   button1 = voxelbotutils.Button("Button 1")
   button2 = voxelbotutils.Button("Button 2")
   components = voxelbotutils.MessageComponents(
      voxelbotutils.ActionRow(button1, button2)
   )
   m = await channel.send("Text is required when sending buttons, unfortunately.", components=components)

Then for all button types other than :attr:`ButtonStyle.LINK`, you can get notified when a user clicks on your button. This is dispatched as a :code:`component_interaction` event.

.. code-block:: python

   payload = await bot.wait_for("component_interaction", check=lambda p: p.message.id == 123123123123)
   await payload.defer()

After that, you can work out which of your buttons the user clicked on and take action based on that, sending back to the button payload so as to complete the interaction.

.. code-block:: python

   clicked_button = p.component
   if clicked_button == button1:
      await p.send("You clicked on button 1!", ephemeral=True)
   elif clicked_button == button2:
      await p.send("You clicked on button 2!", ephemeral=True)

Select Menus
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dropdowns allow the user to select one or more options from a given set.

.. code-block:: python

   button1 = voxelbotutils.Button("Button 1")
   button2 = voxelbotutils.Button("Button 2")
   components = voxelbotutils.MessageComponents(
      voxelbotutils.ActionRow(button1, button2)
   )
   m = await channel.send("Text is required when sending buttons, unfortunately.", components=components)
