import os

import discord

from discord.ext import commands



# Étape 1 : Installation automatique des dépendances

try:

    import pip

    pip.main(['install', 'discord.py'])

except Exception as e:

    print(f"Erreur lors de l'installation des dépendances : {e}")



# Intents requis

intents = discord.Intents.default()

intents.message_content = True

intents.guilds = True

intents.members = True



# Préfixe et instance du bot

bot = commands.Bot(command_prefix="!", intents=intents)



# Variables globales

deleted_messages = {}  # Pour la commande !snipe

role_permissions = {}  # Système de permissions personnalisées



# Événement : quand le bot est prêt

@bot.event

async def on_ready():

    print(f"Bot connecté en tant que {bot.user}!")



# Commande : !help

@bot.command()

async def help(ctx):

    help_message = """

**Crow Bot - Commandes disponibles :**

__**Modération :**__

- !kick <@user> [raison]

- !ban <@user> [raison]

- !unban <id_user>

- !mute <@user> [raison]

- !unmute <@user>

- !warn <@user> [raison]

- !warns <@user>

- !removewarn <@user> <warn_id>

- !clear <nombre>

- !lock

- !unlock

- !slowmode <secondes>

- !snipe

- !pic <@user>

- !banner <@user>



__**Gestion :**__

- !addrole <@user> <@role>

- !removerole <@user> <@role>

- !setnick <@user> <nouveau_nom>

- !serverinfo

- !userinfo <@user>

- !roles

- !createchannel <nom> [text/voice]

- !deletechannel



__**Système de permissions :**__

- !addperm <@role> <perm…>

- !checkperm <@role>

- !removeperm <@role> <perm>

- !listperms



__**Commandes Owner :**__

- !owner

- !shutdown

"""

    await ctx.send(help_message)



# Commande : !owner

@bot.command()

async def owner(ctx):

    app_info = await bot.application_info()

    owner = app_info.owner

    await ctx.send(f"Le propriétaire du bot est : {owner}")



# Commande : !shutdown (ferme le bot)

@bot.command()

@commands.is_owner()

async def shutdown(ctx):

    await ctx.send("Arrêt du bot...")

    await bot.close()



# Commande : !kick

@bot.command()

@commands.has_permissions(kick_members=True)

async def kick(ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):

    await member.kick(reason=reason)

    await ctx.send(f"{member} a été expulsé pour : {reason}")



# Commande : !ban

@bot.command()

@commands.has_permissions(ban_members=True)

async def ban(ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):

    await member.ban(reason=reason)

    await ctx.send(f"{member} a été banni pour : {reason}")



# Commande : !unban

@bot.command()

@commands.has_permissions(ban_members=True)

async def unban(ctx, user_id: int):

    user = await bot.fetch_user(user_id)

    await ctx.guild.unban(user)

    await ctx.send(f"{user} a été débanni.")



# Commande : !mute

@bot.command()

@commands.has_permissions(manage_roles=True)

async def mute(ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):

    overwrite = discord.PermissionOverwrite(send_messages=False, speak=False)

    for channel in ctx.guild.channels:

        await channel.set_permissions(member, overwrite=overwrite)

    await ctx.send(f"{member} a été rendu muet pour : {reason}")



# Commande : !unmute

@bot.command()

@commands.has_permissions(manage_roles=True)

async def unmute(ctx, member: discord.Member):

    for channel in ctx.guild.channels:

        await channel.set_permissions(member, overwrite=None)

    await ctx.send(f"{member} n'est plus muet.")



# Commande : !snipe

@bot.event

async def on_message_delete(message):

    deleted_messages[message.channel.id] = message



@bot.command()

async def snipe(ctx):

    message = deleted_messages.get(ctx.channel.id)

    if message:

        await ctx.send(f"**Auteur** : {message.author}\n**Message** : {message.content}")

    else:

        await ctx.send("Aucun message supprimé trouvé.")



# Commande : !pic

@bot.command()

async def pic(ctx, member: discord.Member = None):

    member = member or ctx.author

    await ctx.send(member.avatar.url)



# Commande : !banner

@bot.command()

async def banner(ctx, member: discord.Member = None):

    member = member or ctx.author

    user = await bot.fetch_user(member.id)

    if user.banner:

        await ctx.send(user.banner.url)

    else:

        await ctx.send("Cet utilisateur n'a pas de bannière.")



# Gestion des erreurs

@bot.event

async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):

        await ctx.send("Vous n'avez pas les permissions nécessaires pour cette commande.")

    elif isinstance(error, commands.MissingRequiredArgument):

        await ctx.send("Argument manquant. Vérifiez la commande.")

    elif isinstance(error, commands.BadArgument):

        await ctx.send("Argument invalide. Vérifiez la commande.")

    else:

        await ctx.send("Une erreur s'est produite.")



# Lancement du bot

TOKEN = os.getenv("DISCORD_TOKEN")  # Récupérer le token depuis les variables Railway

if not TOKEN:

    TOKEN = input("Veuillez entrer votre token Discord : ")

bot.run(TOKEN)