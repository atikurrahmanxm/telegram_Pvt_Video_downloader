@echo off
echo ========================================================
echo   Telegram Pro Downloader - স্পিড ও প্যাকেজ ইনস্টলেশন
echo ========================================================
echo.
echo [1/3] Telethon এবং Flask আপডেট হচ্ছে...
pip install telethon flask --quiet
echo.
echo [2/3] হাই-স্পিড প্যারালাল ইঞ্জিন ইনস্টল হচ্ছে...
pip install FastTelethonhelper --quiet
echo.
echo [3/3] Native C Crypto অ্যাক্সিলারেশন (tgcrypto) ইনস্টল হচ্ছে...
pip install telethon-tgcrypto tgcrypto --quiet
echo.
echo ========================================================
echo   ✅ সম্পূর্ণ সেটআপ ও স্পিড অপ্টিমাইজেশন সম্পন্ন!
echo ========================================================
echo.
echo এখন 4_run_web.bat ফাইলটি ডাবল ক্লিক করে চালু করুন।
echo.
pause
