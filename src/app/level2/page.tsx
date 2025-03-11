"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Particles } from "@/components/magicui/particles";
import { MagicCard } from "@/components/magicui/magic-card";

export default function Level2() {
  const [input, setInput] = useState("");
  const [isCorrect, setIsCorrect] = useState(false);
  const router = useRouter();

  const encryptedText = "LXFOPVEFRNHR"; // Example Vigenère Cipher text
  const correctAnswer = "HELLOWORLD"; // Change this to your actual expected answer

  const handleSubmit = () => {
    if (input.toUpperCase() === correctAnswer) {
      setIsCorrect(true);
      setTimeout(() => router.push("/level3"), 2000);
    } else {
      alert("The cipher mocks your ignorance... Try again.");
    }
  };

  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white px-8 overflow-hidden">
      {/* Particles Background */}
      <Particles className="absolute inset-0 z-0" quantity={80} ease={80} color="#8f98a0" refresh />

      {/* Main Content */}
      <motion.div
        className="relative z-10 flex flex-col items-center space-y-6"
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1.5, ease: "easeOut" }}
      >
        {/* Heading with MagicCard */}
        <MagicCard border glow className="p-6 rounded-lg shadow-lg">
          <h1 className="text-4xl font-bold text-center bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 bg-clip-text text-transparent">
            Level 2 - The Whispering Code
          </h1>
        </MagicCard>

        <p className="text-lg text-neutral-300 text-center italic">
          "The voices are trapped within the cipher. Can you hear them? Can you set them free?"
        </p>

        {/* Encrypted Text Display */}
        <MagicCard border glow>
          <div className="p-4 bg-gray-800 rounded-lg shadow-lg text-center">
            <h2 className="text-2xl font-mono text-purple-300 tracking-widest">{encryptedText}</h2>
          </div>
        </MagicCard>

        {/* Input Field */}
        <motion.input
          type="text"
          placeholder="Whisper the answer..."
          className="p-2 text-black rounded border border-gray-600 shadow-lg w-64 text-center"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          initial={{ scale: 0.9 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.5 }}
        />

        {/* Submit Button */}
        <MagicCard border glow>
          <motion.button
            onClick={handleSubmit}
            className="px-6 py-2 bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500 
                      hover:from-pink-600 hover:via-red-600 hover:to-yellow-600 
                      text-white font-semibold rounded transition shadow-md"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
          >
            Submit
          </motion.button>
        </MagicCard>

        {/* Success Message */}
        {isCorrect && (
          <motion.p
            className="text-green-400 text-lg animate-pulse"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            ✅ "The voices grow silent. You have seen through the illusion… Move forward."
          </motion.p>
        )}
      </motion.div>
    </div>
  );
}
