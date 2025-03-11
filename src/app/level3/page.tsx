"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Particles } from "@/components/magicui/particles";
import { MagicCard } from "@/components/magicui/magic-card";

export default function Level3() {
  const [message, setMessage] = useState("");
  const [isCorrect, setIsCorrect] = useState(false);
  const router = useRouter();

  const correctMessage = "foundpassword123"; // Change this to match your PCAP analysis result

  const handleSubmit = () => {
    if (message.toLowerCase() === correctMessage) {
      setIsCorrect(true);
      setTimeout(() => router.push("/level4"), 2000);
    } else {
      alert("The data eludes you... Seek deeper.");
    }
  };

  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white px-8 overflow-hidden">
      {/* Particles Background */}
      <Particles className="absolute inset-0 z-0" quantity={100} color="#7289da" />

      {/* Main Content */}
      <motion.div
        className="relative z-10 flex flex-col items-center space-y-6"
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1.5, ease: "easeOut" }}
      >
        {/* Heading */}
        <MagicCard border glow className="p-6 rounded-lg shadow-lg">
          <h1 className="text-4xl font-bold text-center bg-gradient-to-r from-blue-400 via-cyan-500 to-teal-500 bg-clip-text text-transparent">
            Level 3 - The Silent Signals
          </h1>
        </MagicCard>

        <p className="text-lg text-neutral-300 text-center italic">
          "The network whispers its secrets, but only those who listen will hear the truth."
        </p>

        {/* File Upload */}
        <MagicCard border glow>
          <input
            type="file"
            accept=".pcap"
            className="p-2 text-black bg-white rounded border border-gray-600"
          />
        </MagicCard>

        {/* Input Field */}
        <motion.input
          type="text"
          placeholder="What have you uncovered?"
          className="p-2 text-black rounded border border-gray-600 shadow-lg w-64 text-center"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          initial={{ scale: 0.9 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.5 }}
        />

        {/* Submit Button */}
        <MagicCard border glow>
          <motion.button
            onClick={handleSubmit}
            className="px-6 py-2 bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500 
                      hover:from-cyan-600 hover:via-blue-600 hover:to-purple-600 
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
            ✅ "The transmissions fade… You have deciphered the ghostly echoes. Move forward."
          </motion.p>
        )}
      </motion.div>
    </div>
  );
}