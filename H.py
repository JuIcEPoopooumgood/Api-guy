    @commands.command(
        description="List the developers", name="devs", aliases=["dev", "creators"]
    )
    async def devs_command(self, ctx, dev=None):
        data_url = "https://juicepoopooumgood.github.io/Api-guy/Devs/index.json"
        data = requests.get(data_url).json()
        # data is structured like this: [
        #   {
        #     "User": "Glitchy",
        #     "ID": 1236667927944761396,
        #     "kirkaid": "B0TMFC",
        #     "Added": "Main developer of the bot",
        #     "Role": "Owner/Lead Dev"
        #   },
        devs_table = [
            {
                "Name": "Glitchy",
                "Matches": ["glitch", "glitchy", "err", "500"],
                "URL": "https://juicepoopooumgood.github.io/Api-guy/glitchy.json",
            },
            {
                "Name": "Poopoumgood",
                "Matches": ["ppg", "ppgyt", "poop", "ppug", "ppugyt"],
                "URL": "https://api.lanyard.rest/v1/users/1169111190824308768",
            },
        ]
        if dev:
            dev_table_entry = None
            for entry in devs_table:
                if dev.lower() in [match.lower() for match in entry["Matches"]]:
                    dev_table_entry = entry
            if not dev_table_entry:
                await ctx.reply(
                    "Contributor not found. Maybe they dont have a page registered."
                )
                return
            dev_profile = requests.get(dev_table_entry["URL"]).json()
            if dev_profile["Color"] == "random":
                color = discord.Color.random()
            else:
                color = discord.Color.from_rgb(*hex_to_rgb(dev_profile["Color"]))
            embed = discord.Embed(
                color=color,
                title=dev_profile["User"],
            )
            print(dev_profile)
            embed.add_field(name="username:", value=f"<@{dev_profile['id']}>")
            embed.add_field(name="Kirka ID:  ", value=dev_profile["tag"])
            embed.set_footer(
                text=dev_profile["created_at"], icon_url=dev_profile["https://cdn.discordapp.com/avatars/1169111190824308768/d607ee718dab50611ab0867908766b90.png?size=4096"]
            )
            for i in range(10):  # Adjust range if there could be more than 10 entries
                text_key = f"Text{i}"
                title_key = f"Title{i}"

                if text_key in dev_profile:  # Only add if the text key exists
                    field_title = (
                        dev_profile[title_key]
                        if title_key in dev_profile
                        else ("About:" if i == 0 else f"- -{i}")
                    )

                    embed.add_field(
                        name=field_title,
                        value=dev_profile[text_key],
                        inline=False,
                    )
            title_img, title_name = None, None
            if "title_img" in dev_profile:
                title_img = dev_profile["title_img"]
            if "title_name" in dev_profile:
                title_name = dev_profile["title_name"]
            embed.set_author(name=title_name, icon_url=title_img)

            await ctx.send(embed=embed)
            return

        embed = discord.Embed(color=discord.Color.random(), title="Developers")
        for i in data:
            embed.add_field(
                name=f"{i['username']} #{i['tag']}",
                value=f"<@{i['id']}>\nContribution: {i['discord_status']}\nRole: {i['state']}",
            )
        await ctx.reply(embed=embed)
