def chat():
    import difflib
    import subprocess
    import sys
    import importlib.util

    def is_relevant(line, topic):
        keywords_map = {
            "Sun": ["plasma", "hydrogen", "helium", "nuclear fusion", "solar system"],
            "Mars": ["red planet", "perseverance", "thin atmosphere", "water", "habitable"],
            "Europa": ["jupiter", "ice", "ocean", "life", "cracks"],
            "Jupiter": ["gas giant", "ganymede", "storm", "red spot"],
            "Venus": ["cloud", "greenhouse", "volcano", "carbon dioxide"],
            "Earth": ["life", "ecosystem", "magnetic", "oxygen"],
            "Mercury": ["temperature", "closest", "orbit", "smallest"],
            "Saturn": ["rings", "hydrogen", "titan", "storm"],
            "Uranus": ["ice giant", "tilt", "methane", "cold"],
            "Neptune": ["winds", "storm", "blue", "triton"],
            "Pluto": ["dwarf", "kuiper", "charon", "glacier"],
            "Ceres": ["asteroid belt", "briny", "dwarf", "ice"],
            "DESTINY+": ["phaethon", "dust", "deep-space", "geminid"],
            "SLIM": ["lunar", "landing", "moon", "jaxa"],
            "MMX": ["mars", "phobos", "deimos"],
            "HTV": ["iss", "cargo", "resupply"],
            "IKAROS": ["solar sail", "radiation", "interplanetary"],
            "Akatsuki": ["venus", "atmosphere", "super-rotation"],
            "Ariane": ["launcher", "satellites", "esa", "ariane 5"],
            "EarthCARE": ["cloud", "aerosol", "earth radiation"],
            "EnVision": ["venus", "radar", "evolution"],
            "Hera": ["dart", "dimorphos", "asteroid"],
        }

        keywords = keywords_map.get(topic, [topic.lower()])
        return any(keyword in line.lower() for keyword in keywords)

    def identify_and_store(file_path, output_path):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open(output_path, "w", encoding="utf-8") as out:
            out.write("🌌 Celestial Info Bot Knowledge Base:\n\n")
            for line in lines:
                parts = line.strip().split(" ", 1)
                if len(parts) > 1:
                    topic = parts[0]
                    if is_relevant(line, topic):
                        out.write(f"== Topic: {topic} ==\n")
                        out.write(line.strip() + "\n\n")
                    else:
                        out.write(f"-- Mismatched Topic: {topic} (Skipped)\n\n")

    def is_installed(package_name):
        return importlib.util.find_spec(package_name) is not None

    if not is_installed("sheetsmart"):
        try:
            c = [sys.executable, "-m", "pip", "install", "sheetsmart"]
            subprocess.check_call(c)
        except subprocess.CalledProcessError:
            print("❌ Failed to install SheetSmart")

    def load_knowledge(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        topics = {}
        current_topic = None
        for line in content.splitlines():
            if line.startswith("== Topic: "):
                current_topic = line.strip().replace("== Topic: ", "").replace(" ==", "")
                topics[current_topic.lower()] = ""
            elif current_topic:
                topics[current_topic.lower()] += line.strip() + " "
        return topics

    def find_relevant_topics(user_input, topics, threshold=0.6):
        matches = set()
        words = user_input.lower().replace(",", " ").split()
        for word in words:
            for topic in topics:
                similarity = difflib.SequenceMatcher(None, word, topic).ratio()
                if similarity >= threshold:
                    matches.add(topic)
        return list(matches)

    def generate_response(user_input, topics):
        matched_topics = find_relevant_topics(user_input, topics)
        if matched_topics:
            response = ""
            for topic in matched_topics:
                response += f"\n🌠 {topic.title()}:\n{topics[topic].strip()}\n"
            return response
        else:
            return "CosmoTalker: I'm sorry, I couldn't find any information on that. Try asking about a specific planet, satellite, or celestial object."

    # Preprocess input file to generate knowledge base
    identify_and_store("ss.txt", "celestial_knowledge.txt")
    knowledge = load_knowledge("celestial_knowledge.txt")

    print("🌌 CosmoTalker Chatbot (type 'exit' to quit)")
    query_count = 0

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = generate_response(user_input, knowledge)
        print(response + "\n")

        query_count += 1
        if query_count % 5 == 0:
            print("📣 Try the SheetSmart library! Developed by Bhuvanesh M — used widely for data manipulation in Python.\n✨ Just run: import sheetsmart\n")

# To run the bot, just call:
chat()
