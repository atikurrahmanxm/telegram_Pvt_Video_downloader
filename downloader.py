"""
Telegram Video Downloader
আপনার নিজের কেনা কোর্সের ভিডিও ডাউনলোড করার টুল।
Telethon ব্যবহার করে আপনার নিজের অ্যাকাউন্ট দিয়ে লগইন করে।
"""

import os
import asyncio
from telethon import TelegramClient
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto
import sys

# ============================================================
#  এখানে আপনার API তথ্য বসান (config.py ফাইল থেকে নেওয়া হবে)
# ============================================================
try:
    from config import API_ID, API_HASH, PHONE_NUMBER
except ImportError:
    print("❌ config.py ফাইল পাওয়া যায়নি!")
    print("   config.py ফাইল তৈরি করুন (নিচের নির্দেশনা দেখুন)।")
    sys.exit(1)

# ডাউনলোড করা ফাইল কোথায় সেভ হবে
DOWNLOAD_FOLDER = "downloaded_videos"


async def list_groups(client):
    """আপনার সব গ্রুপ ও চ্যানেলের তালিকা দেখাবে"""
    print("\n📋 আপনার গ্রুপ ও চ্যানেলের তালিকা:\n")
    dialogs = await client.get_dialogs()
    groups = []
    for i, dialog in enumerate(dialogs):
        if dialog.is_group or dialog.is_channel:
            groups.append(dialog)
            print(f"  [{i+1}] {dialog.name}  (ID: {dialog.id})")
    return groups


async def download_videos_from_group(client, group):
    """নির্দিষ্ট গ্রুপ থেকে সব ভিডিও ডাউনলোড করবে"""

    # ডাউনলোড ফোল্ডার তৈরি করো
    group_folder = os.path.join(DOWNLOAD_FOLDER, str(group.name))
    os.makedirs(group_folder, exist_ok=True)

    print(f"\n🔍 '{group.name}' গ্রুপের ভিডিও খোঁজা হচ্ছে...\n")

    video_count = 0
    downloaded = 0

    # গ্রুপের সব মেসেজ স্ক্যান করো
    async for message in client.iter_messages(group, limit=None):
        # শুধু ভিডিও মেসেজ খোঁজো
        if message.media and isinstance(message.media, MessageMediaDocument):
            doc = message.media.document
            # ভিডিও কিনা চেক করো
            is_video = any(
                attr.__class__.__name__ == 'DocumentAttributeVideo'
                for attr in doc.attributes
            )
            if is_video:
                video_count += 1
                # ফাইলের নাম বের করো
                file_name = None
                for attr in doc.attributes:
                    if hasattr(attr, 'file_name') and attr.file_name:
                        file_name = attr.file_name
                        break
                if not file_name:
                    file_name = f"video_{message.id}.mp4"

                file_path = os.path.join(group_folder, file_name)

                # আগে ডাউনলোড হয়ে থাকলে স্কিপ করো
                if os.path.exists(file_path):
                    print(f"  ⏭️  আগেই আছে: {file_name}")
                    continue

                print(f"  ⬇️  ডাউনলোড হচ্ছে ({video_count}): {file_name}")

                # ডাউনলোড প্রোগ্রেস দেখানোর জন্য
                def progress_callback(received, total):
                    if total:
                        percent = round((received / total) * 100, 1)
                        print(f"      {percent}% ({round(received/1024/1024, 1)} MB / {round(total/1024/1024, 1)} MB)", end='\r')

                await client.download_media(
                    message,
                    file=file_path,
                    progress_callback=progress_callback
                )
                downloaded += 1
                print(f"\n  ✅ সম্পন্ন: {file_name}")

    print(f"\n🎉 মোট {downloaded}টি ভিডিও ডাউনলোড হয়েছে '{group_folder}' ফোল্ডারে।")


async def main():
    print("=" * 55)
    print("   📥 Telegram Video Downloader")
    print("=" * 55)

    # Telegram Client তৈরি করো
    client = TelegramClient('my_session', API_ID, API_HASH)

    async with client:
        # লগইন করো (প্রথমবার OTP আসবে)
        await client.start(phone=PHONE_NUMBER)
        print(f"\n✅ সফলভাবে লগইন হয়েছে!\n")

        # গ্রুপের তালিকা দেখাও
        groups = await list_groups(client)

        if not groups:
            print("কোনো গ্রুপ বা চ্যানেল পাওয়া যায়নি।")
            return

        # ব্যবহারকারীকে গ্রুপ বেছে নিতে বলো
        print(f"\nমোট {len(groups)}টি গ্রুপ/চ্যানেল পাওয়া গেছে।")
        choice = input("\nকোন নম্বরের গ্রুপ থেকে ডাউনলোড করবেন? নম্বর লিখুন: ").strip()

        try:
            choice_idx = int(choice) - 1
            selected_group = groups[choice_idx]
        except (ValueError, IndexError):
            print("❌ ভুল নম্বর দেওয়া হয়েছে।")
            return

        print(f"\n✅ নির্বাচিত: '{selected_group.name}'")
        confirm = input("এই গ্রুপ থেকে সব ভিডিও ডাউনলোড শুরু করবেন? (yes/no): ").strip().lower()

        if confirm in ['yes', 'y', 'হ্যাঁ']:
            await download_videos_from_group(client, selected_group)
        else:
            print("বাতিল করা হয়েছে।")


if __name__ == "__main__":
    asyncio.run(main())

