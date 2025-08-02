from confluence import fetch_confluence_page, ask_confluence_question

def main():
    page_id = input("🔢 Confluence Page ID: ")
    question = input("💬 Your question: ")

    print("📥 Fetching page...")
    try:
        content = fetch_confluence_page(page_id)
        print("✅ Page fetched.")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    print("🤖 Asking Groq...")
    answer = ask_confluence_question(question, content)
    print("\n🧠 Answer:\n")
    print(answer)

if __name__ == "__main__":
    main()