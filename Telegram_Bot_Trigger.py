# import os
# import asyncio
# from dotenv import load_dotenv
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import ContextTypes
#
# # Import all our decoupled pipeline modules
# from Travily_Niche_Research import run_initial_research
# from Title_Planner_Agent import run_planner_agent
# from Topics_Split import generate_all_sections
# from HTML_Editor_Agent import run_editor_agent
# from Gmail_Draft import create_gmail_draft
# from Blogger_Published import publish_to_blogger
#
# load_dotenv()
#
# # Global in-memory data store to retain structured layout data awaiting user approval
# DRAFTS_STORE = {}
#
#
# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Handles the /start command."""
#     welcome_message = (
#         "🤖 Welcome to your Multi-Agent Newsletter Automator!\n\n"
#         "Send me a niche topic (e.g., 'AI adoption for small businesses') "
#         "to trigger the pipeline."
#     )
#     await update.message.reply_text(welcome_message)
#
#
# async def handle_message_with_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Handles incoming text messages and coordinates the core multi-agent execution loop."""
#     user_text = update.message.text
#     user_info = update.message.from_user.username or update.message.from_user.first_name
#
#     # Detailed Console Logging
#     print(f"\n{'=' * 60}")
#     print(f"🚀 PIPELINE EXECUTION STARTED BY USER: {user_info}")
#     print(f"🎯 Target Niche: '{user_text}'")
#     print(f"{'=' * 60}")
#
#     try:
#         loop = asyncio.get_running_loop()
#
#         # --- STEP 1: INITIAL RESEARCH (TAVILY) ---
#         print("\n[Step 1/6] 🔍 Initiating broad Tavily niche discovery...")
#         await update.message.reply_text(f"🔍 [Step 1/6] Running Tavily search for '{user_text}'...")
#
#         search_results = await loop.run_in_executor(None, run_initial_research, user_text)
#
#         if not search_results:
#             print("[Step 1/6] ⚠️ Execution halted: No relevant articles returned from Tavily.")
#             await update.message.reply_text(
#                 "⚠️ Search completed, but no relevant articles were found. Try another niche.")
#             return
#
#         print(f"[Step 1/6] ✅ Research phase complete. Retrieved {len(search_results)} primary sources.")
#         await update.message.reply_text(f"✅ [Step 1/6] Found {len(search_results)} articles.")
#
#         # --- STEP 2: PLANNER AGENT (GEMINI) ---
#         print("\n[Step 2/6] 🧠 Invoking Planner Agent to determine structural layout...")
#         await update.message.reply_text("🧠 [Step 2/6] Planner Agent is drafting title and topics...")
#
#         plan = await loop.run_in_executor(None, run_planner_agent, search_results)
#
#         print("[Step 2/6] ✅ Structured planning parsing complete.")
#         print(f"  -> Title: {plan['title']}")
#         for idx, topic in enumerate(plan['topics'], 1):
#             print(f"  -> Selected Topic {idx}: {topic}")
#
#         reply_plan = (
#             "✅ **Planning Complete!**\n\n"
#             f"📰 **Draft Title:** {plan['title']}\n\n"
#             "📌 **Selected Topics:**\n"
#         )
#         for idx, topic in enumerate(plan['topics'], 1):
#             reply_plan += f"{idx}. {topic}\n"
#
#         await update.message.reply_text(reply_plan, parse_mode="Markdown")
#
#         # --- STEP 3 & 4: SPLIT OUT, DEEP RESEARCH & SECTION WRITING ---
#         print("\n[Step 3 & 4/6] ⏳ Splitting tasks and spawning concurrent worker pools...")
#         await update.message.reply_text(
#             "⏳ [Step 3 & 4/6] Deep researching topics and writing sections concurrently (this takes a moment)...")
#
#         sections = await generate_all_sections(plan['topics'])
#
#         print("[Step 3 & 4/6] ✅ Content collection and Markdown drafting complete.")
#         print("--- 📝 Dynamic Section Preview ---")
#         for i, section in enumerate(sections, 1):
#             print(f"\n[Section {i}]\n{section[:120]}...\n")
#         print("---------------------------------")
#
#         await update.message.reply_text(
#             "✅ [Step 3 & 4/6] All 3 newsletter sections successfully written and aggregated!")
#
#         # --- STEP 5: EDITOR AGENT (HTML COMPILE) ---
#         print("\n[Step 5/6] 🎨 Launching Editor Agent for responsive HTML generation...")
#         await update.message.reply_text("⏳ [Step 5/6] Editor Agent is generating the final HTML...")
#
#         final_newsletter = await loop.run_in_executor(None, run_editor_agent, plan['title'], sections)
#
#         print("[Step 5/6] ✅ Production layout design finalized.")
#         print(f"  -> Subject Line: {final_newsletter['subject']}")
#         print(f"  -> HTML Output Size: {len(final_newsletter['content'])} characters.\n")
#
#         reply_editor = (
#             "✅ **Newsletter Successfully Generated!**\n\n"
#             f"📧 **Subject Line:** `{final_newsletter['subject']}`\n\n"
#             "💻 *The raw HTML source layout has been logged to your console.*"
#         )
#         await update.message.reply_text(reply_editor, parse_mode="Markdown")
#
#         # --- STEP 6: GMAIL DRAFT STAGING ---
#         print("\n[Step 6/6] 📧 Contacting Gmail API to stage draft...")
#         await update.message.reply_text("⏳ [Step 6/6] Connecting to Gmail to save the draft...")
#
#         draft_id = await loop.run_in_executor(
#             None,
#             create_gmail_draft,
#             final_newsletter['subject'],
#             final_newsletter['content'],
#             ""
#         )
#
#         if draft_id:
#             print(f"[Step 6/6] 🎉 Gmail payload staged successfully. Remote Reference ID: {draft_id}")
#
#             # Persist the dynamic context mapped to the remote draft ID
#             DRAFTS_STORE[draft_id] = {
#                 "title": plan['title'],
#                 "content": final_newsletter['content']
#             }
#
#             # Pack transaction data natively inside the interactive markup buttons
#             keyboard = [
#                 [
#                     InlineKeyboardButton("✅ Approve & Publish", callback_data=f"approve_{draft_id}"),
#                     InlineKeyboardButton("❌ Reject", callback_data=f"reject_{draft_id}"),
#                 ]
#             ]
#             reply_markup = InlineKeyboardMarkup(keyboard)
#
#             final_reply = (
#                 "🎉 **Newsletter Draft Successfully Created in Gmail!**\n\n"
#                 f"📧 **Subject:** `{final_newsletter['subject']}`\n"
#                 f"📂 **Draft ID:** `{draft_id}`\n\n"
#                 "Please check your Gmail inbox. Do you approve publishing this edition live to Blogger?"
#             )
#             await update.message.reply_text(final_reply, parse_mode="Markdown", reply_markup=reply_markup)
#         else:
#             print("[Step 6/6] ❌ API Error: Gmail transaction rejected.")
#             await update.message.reply_text("❌ Failed to create the Gmail draft. Check your terminal for errors.")
#
#     except Exception as e:
#         print(f"\n❌ Pipeline exception caught during execution loop: {e}")
#         await update.message.reply_text(f"❌ An error occurred: {e}")
#
#
# # --- INLINE KEYBOARD REACTION HANDLERS ---
# async def handle_approval(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Processes interactive callback events triggered by user choice approvals."""
#     query = update.callback_query
#     await query.answer()
#
#     data = query.data
#     action, draft_id = data.split("_", 1)
#
#     if action == "approve":
#         print(f"\n[Human in the Loop] -> User APPROVED publication route for draft identifier: {draft_id}.")
#         await query.edit_message_text(text="✅ **Draft Approved!** Uploading data streams directly to Blogger... ⏳")
#
#         # Verify state persistence validation checks
#         draft_data = DRAFTS_STORE.get(draft_id)
#         if not draft_data:
#             print("❌ State Error: Active context cache block missing from local memory register.")
#             await query.edit_message_text(
#                 text="❌ **Error:** Content cache expired from application memory. Please run the generation loop again.")
#             return
#
#         # Execute publishing sequences off the main async event loop
#         loop = asyncio.get_running_loop()
#         print(f"🌐 [Publishing Engine] Connecting to Blogger to create post: '{draft_data['title']}'...")
#         public_url = await loop.run_in_executor(
#             None,
#             publish_to_blogger,
#             draft_data["title"],
#             draft_data["content"]
#         )
#
#         if public_url:
#             print(f"🎉 [Publishing Engine] Live deploy successful! Route: {public_url}")
#             success_msg = (
#                 "🌍 **Blog Published Successfully!**\n\n"
#                 f"🔗 **Live Link:** {public_url}\n\n"
#                 "State stored. Ready for social media processing."
#             )
#             await query.edit_message_text(text=success_msg, parse_mode="Markdown")
#
#             # Clean up the memory register cleanly
#             del DRAFTS_STORE[draft_id]
#         else:
#             print("❌ [Publishing Engine] Critical Error: remote insert execution failed.")
#             await query.edit_message_text(
#                 text="❌ **Failed to publish to Blogger.** Please examine server terminal console error logs.")
#
#     elif action == "reject":
#         print(f"\n[Human in the Loop] -> User REJECTED transaction frame: {draft_id}.")
#         await query.edit_message_text(
#             text="❌ **Draft was rejected.** The transaction has been purged. Send a new topic topic to start fresh.")
#         if draft_id in DRAFTS_STORE:
#             del DRAFTS_STORE[draft_id]


import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Import all decoupled pipeline modules
from Travily_Niche_Research import run_initial_research
from Title_Planner_Agent import run_planner_agent
from Topics_Split import generate_all_sections
from HTML_Editor_Agent import run_editor_agent
from Gmail_Draft import create_gmail_draft
from Blogger_Published import publish_to_blogger
from Social_Agent import run_social_agent

load_dotenv()

# Global in-memory data store for drafts
DRAFTS_STORE = {}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    welcome_message = (
        "🤖 Welcome to your Master Newsletter Automator!\n\n"
        "Send me a niche topic (e.g., 'AI adoption for small businesses') "
        "to trigger the end-to-end pipeline."
    )
    await update.message.reply_text(welcome_message)


async def handle_message_with_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles incoming text messages and coordinates Phase 1 (Research -> Gmail)."""
    user_text = update.message.text
    user_info = update.message.from_user.username or update.message.from_user.first_name

    print(f"\n{'=' * 60}")
    print(f"🚀 PIPELINE EXECUTION STARTED BY USER: {user_info}")
    print(f"🎯 Target Niche: '{user_text}'")
    print(f"{'=' * 60}")

    try:
        loop = asyncio.get_running_loop()

        # --- STEP 1: INITIAL RESEARCH ---
        print("\n[Step 1/6] 🔍 Running Tavily search...")
        msg1 = await update.message.reply_text(f"🔍 [Step 1/6] Running Tavily search for '{user_text}'...")

        search_results = await loop.run_in_executor(None, run_initial_research, user_text)
        if not search_results:
            await msg1.edit_text("⚠️ No relevant articles were found. Try another niche.")
            return

        # --- STEP 2: PLANNER AGENT ---
        print("\n[Step 2/6] 🧠 Planner Agent drafting...")
        await msg1.edit_text("🧠 [Step 2/6] Planner Agent is drafting title and topics...")

        plan = await loop.run_in_executor(None, run_planner_agent, search_results)

        # --- STEP 3 & 4: SPLIT OUT & WRITING ---
        print("\n[Step 3 & 4/6] ⏳ Deep researching and writing concurrently...")
        await msg1.edit_text("⏳ [Step 3 & 4/6] Deep researching topics and writing sections concurrently...")

        sections = await generate_all_sections(plan['topics'])

        # --- STEP 5: EDITOR AGENT ---
        print("\n[Step 5/6] 🎨 Editor Agent generating HTML...")
        await msg1.edit_text("⏳ [Step 5/6] Editor Agent is generating the final HTML...")

        final_newsletter = await loop.run_in_executor(None, run_editor_agent, plan['title'], sections)

        # --- STEP 6: GMAIL DRAFT STAGING ---
        print("\n[Step 6/6] 📧 Contacting Gmail API...")
        await msg1.edit_text("⏳ [Step 6/6] Connecting to Gmail to save the draft...")

        draft_id = await loop.run_in_executor(
            None, create_gmail_draft, final_newsletter['subject'], final_newsletter['content'], ""
        )

        if draft_id:
            print(f"[Step 6/6] 🎉 Gmail payload staged successfully. ID: {draft_id}")

            DRAFTS_STORE[draft_id] = {
                "title": plan['title'],
                "content": final_newsletter['content']
            }

            # Using 'blog_' prefix to distinguish from social buttons
            keyboard = [
                [
                    InlineKeyboardButton("✅ Approve & Publish", callback_data=f"blog_approve_{draft_id}"),
                    InlineKeyboardButton("❌ Reject Draft", callback_data=f"blog_reject_{draft_id}"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            final_reply = (
                "🎉 **Newsletter Draft Created in Gmail!**\n\n"
                f"📧 **Subject:** `{final_newsletter['subject']}`\n\n"
                "Please check your Gmail inbox. Do you approve publishing this edition live to Blogger?"
            )
            await msg1.edit_text(final_reply, parse_mode="Markdown", reply_markup=reply_markup)
        else:
            await msg1.edit_text("❌ Failed to create the Gmail draft. Check your terminal for errors.")

    except Exception as e:
        print(f"\n❌ Pipeline exception: {e}")
        await update.message.reply_text(f"❌ An error occurred: {e}")


# --- INLINE KEYBOARD REACTION HANDLER ---
async def handle_approval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes ALL interactive callback clicks (Both Blogger and Social approvals)."""
    query = update.callback_query
    await query.answer()

    data = query.data
    loop = asyncio.get_running_loop()

    # ==========================================
    # PHASE 1: BLOGGER APPROVAL HANDLING
    # ==========================================
    if data.startswith("blog_"):
        parts = data.split("_", 2)
        action, draft_id = parts[1], parts[2]

        if action == "approve":
            print(f"\n[Human in the Loop] -> User APPROVED publication for: {draft_id}")
            publish_msg = await query.edit_message_text(text="✅ **Draft Approved!** Uploading live to Blogger... ⏳",
                                                        parse_mode="Markdown")

            draft_data = DRAFTS_STORE.get(draft_id)
            if not draft_data:
                await publish_msg.edit_text(text="❌ **Error:** Memory cache expired. Please run again.")
                return

            try:
                # 1. Publish to Blogger
                public_url = await loop.run_in_executor(None, publish_to_blogger, draft_data["title"],
                                                        draft_data["content"])

                if not public_url:
                    await publish_msg.edit_text(text="❌ **Failed to publish to Blogger.** Check console logs.")
                    return

                print(f"🎉 Live deploy successful! Route: {public_url}")
                await publish_msg.edit_text(
                    text=f"🌍 **Blog Published Live!**\n🔗 {public_url}\n\nGenerating Social Media Drafts... ⏳",
                    parse_mode="Markdown")

                # 2. Trigger Social Agent
                print("[Social Agent] 📱 Generating channel-optimized copy...")
                social_posts = await loop.run_in_executor(None, run_social_agent, draft_data["title"],
                                                          draft_data["content"])

                # 3. Format and distribute the 3 distinct Text Messages
                platforms = {
                    "twitter": ("🐦 TWITTER / X DRAFT", social_posts['twitter']),
                    "linkedin": ("💼 LINKEDIN DRAFT", social_posts['linkedin']),
                    "telegram": ("📣 TELEGRAM PROMO DRAFT", social_posts['telegram_promo'])
                }

                for key, (header, post_content) in platforms.items():
                    formatted_message = (
                        f"{header}\n\n"
                        f"{post_content}\n\n"
                        f"Here you can read our blog : {public_url}"
                    )

                    # Using 'soc_' prefix to route clicks to Phase 2
                    keyboard = [
                        [
                            InlineKeyboardButton("✅ Approve", callback_data=f"soc_approve_{key}"),
                            InlineKeyboardButton("❌ Reject", callback_data=f"soc_reject_{key}")
                        ]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)

                    # Note: We use context.bot.send_message to drop new messages into the chat below the Blogger approval
                    await context.bot.send_message(
                        chat_id=query.message.chat_id,
                        text=formatted_message,
                        reply_markup=reply_markup
                    )
                    await asyncio.sleep(0.5)  # Stagger to keep order correct

                # Clean up memory
                del DRAFTS_STORE[draft_id]

            except Exception as e:
                print(f"❌ Error during post-publication processing: {e}")
                await publish_msg.edit_text(text=f"❌ An error occurred after publication: `{str(e)}`",
                                            parse_mode="Markdown")

        elif action == "reject":
            print(f"\n[Human in the Loop] -> User REJECTED draft {draft_id}.")
            await query.edit_message_text(text="❌ **Draft was rejected.** Send a new topic to start fresh.",
                                          parse_mode="Markdown")
            if draft_id in DRAFTS_STORE:
                del DRAFTS_STORE[draft_id]

    # ==========================================
    # PHASE 2: SOCIAL MEDIA APPROVAL HANDLING
    # ==========================================
    elif data.startswith("soc_"):
        parts = data.split("_", 2)
        action, platform_type = parts[1], parts[2]
        platform_name = platform_type.upper()

        if action == "approve":
            print(f"\n[Human in the Loop] -> Approved social post: {platform_name}")

            # Smart Channel Broadcasting Logic for Telegram
            if platform_type == "telegram":
                approved_text = query.message.text
                channel_id = os.getenv("TELEGRAM_CHANNEL_ID")

                if channel_id:
                    try:
                        await context.bot.send_message(chat_id=channel_id, text=approved_text)
                        await query.edit_message_text(
                            text=f"✅ **{platform_name} Post Approved & Published to {channel_id}!**",
                            parse_mode="Markdown")
                        print(f"🚀 Successfully broadcasted to {channel_id}")
                    except Exception as e:
                        print(f"❌ Failed to post to channel: {e}")
                        await query.edit_message_text(
                            text=f"❌ **Failed to publish:** Is the bot an Admin in {channel_id}?",
                            parse_mode="Markdown")
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text=f"📢 [SIMULATED BROADCAST - Add TELEGRAM_CHANNEL_ID to .env]\n\n{approved_text}")
                    await query.edit_message_text(text=f"✅ **{platform_name} Post Approved (Simulated)!**",
                                                  parse_mode="Markdown")

            else:
                # Normal approval update for Twitter/LinkedIn text blocks
                await query.edit_message_text(text=f"✅ **{platform_name} Post Approved!**", parse_mode="Markdown")

        elif action == "reject":
            print(f"\n[Human in the Loop] -> Rejected social post: {platform_name}")
            await query.edit_message_text(text=f"❌ **{platform_name} Post Rejected!**", parse_mode="Markdown")


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found.")
        return

    print("🤖 Starting Master Automation Pipeline...")
    print("Waiting for commands...")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message_with_search))

    # We now point to the master handle_callback function
    app.add_handler(CallbackQueryHandler(handle_callback))

    app.run_polling()


if __name__ == "__main__":
    main()