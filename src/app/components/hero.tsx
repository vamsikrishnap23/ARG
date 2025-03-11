"use client";
import { Particles } from "@/components/magicui/particles";
import Link from "next/link";
import { buttonVariants } from "@/components/ui/button";
import { ArrowTopRightIcon, MagnifyingGlassIcon } from "@radix-ui/react-icons";

export default function Hero() {
  return (
    <div className="flex items-center justify-center h-screen px-8">
      <Particles
        className="absolute inset-0 -z-10"
        quantity={40}
        ease={80}
        color="#e3ecfa"
        refresh
      />
      <div className="flex flex-col items-center justify-center min-h-screen text-center px-6 mt-12">
        <h2 className="text-3xl md:text-7xl tracking-tighter max-w-5xl mx-auto">
          some things aren’t meant to be{" "}
          <span className="bg-gradient-to-r from-cyan-300 via-blue-500 to-indigo-400 bg-clip-text text-transparent text-shadow-lg">
            remembered.
          </span>
        </h2>
        <p className="text-lg font-extralight md:text-xl text-neutral-400 max-w-2xl mt-6">
          a name. a place. a moment. lost in between.
        </p>

        {/* Updated Button Section */}
        <div className="mt-8">
          <Link
            className={buttonVariants({
              variant: "outline",
              size: "icon",
              className: "px-4 py-4 !rounded-full",
            })}
            href="/level1" // Changed from "/get-started" to "/level1"
          >
            <MagnifyingGlassIcon className="w-16 h-16" />
          </Link>
        </div>
      </div>
    </div>
  );
}
