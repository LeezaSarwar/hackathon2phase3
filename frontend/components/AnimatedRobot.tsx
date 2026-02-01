"use client";

import { useEffect, useState } from "react";

interface AnimatedRobotProps {
  imageUrl?: string;
}

export default function AnimatedRobot({ imageUrl }: AnimatedRobotProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="relative w-full h-[280px] sm:h-[320px] md:h-[380px] lg:h-[420px] flex items-center justify-center">
      {/* Glowing base platform */}
      <div className="absolute bottom-0 w-40 sm:w-48 md:w-64 h-4 bg-gradient-to-r from-transparent via-indigo-500/30 to-transparent rounded-full blur-xl animate-pulse-slow" />

      {/* Outer glow ring - pulsing */}
      <div className="absolute inset-0 flex items-center justify-center animate-pulse-glow">
        <div className="w-52 h-52 sm:w-64 sm:h-64 md:w-80 md:h-80 lg:w-96 lg:h-96 rounded-full bg-gradient-to-r from-indigo-500/20 via-purple-500/20 to-pink-500/20 blur-3xl" />
      </div>

      {/* Orbital rings */}
      <div className="absolute inset-0 flex items-center justify-center animate-spin-slow">
        <div className="w-48 h-48 sm:w-56 sm:h-56 md:w-72 md:h-72 lg:w-80 lg:h-80 rounded-full border-2 border-dashed border-indigo-300/30" />
      </div>
      <div className="absolute inset-0 flex items-center justify-center animate-spin-reverse">
        <div className="w-40 h-40 sm:w-48 sm:h-48 md:w-64 md:h-64 lg:w-72 lg:h-72 rounded-full border-2 border-dotted border-purple-300/30" />
      </div>

      {/* Floating todo elements */}
      {mounted && (
        <>
          {/* Floating task card */}
          <div className="absolute top-16 left-1/4 w-12 h-8 bg-white/20 backdrop-blur-sm rounded-lg border border-white/30 animate-float-particle-1 flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>

          {/* Floating plus icon */}
          <div className="absolute top-28 right-1/4 w-6 h-6 bg-green-400/30 backdrop-blur-sm rounded-full animate-float-particle-2 flex items-center justify-center">
            <svg className="w-3 h-3 text-green-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M12 4v16m8-8H4" />
            </svg>
          </div>

          {/* Floating calendar */}
          <div className="absolute bottom-28 left-1/3 w-8 h-8 bg-blue-400/30 backdrop-blur-sm rounded-md animate-float-particle-3 flex items-center justify-center">
            <svg className="w-4 h-4 text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>

          {/* Floating priority indicator */}
          <div className="absolute bottom-20 right-1/3 w-6 h-6 bg-red-400/30 backdrop-blur-sm rounded-full animate-float-particle-4 flex items-center justify-center">
            <svg className="w-3 h-3 text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>

          {/* Floating completed task */}
          <div className="absolute top-1/3 left-20 w-8 h-8 bg-green-400/30 backdrop-blur-sm rounded-lg animate-float-particle-1 flex items-center justify-center">
            <svg className="w-4 h-4 text-green-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>

          {/* Floating edit icon */}
          <div className="absolute top-1/2 right-20 w-6 h-6 bg-yellow-400/30 backdrop-blur-sm rounded-full animate-float-particle-3 flex items-center justify-center">
            <svg className="w-3 h-3 text-yellow-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </div>
        </>
      )}

      {/* Main robot container - floating animation */}
      <div className="relative z-10 animate-float-smooth">
        {/* Robot body with glassmorphism */}
        <div className="relative w-32 h-32 sm:w-40 sm:h-40 md:w-48 md:h-48 lg:w-56 lg:h-56 animate-tilt-3d">
          {/* Glow effect behind robot */}
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 rounded-3xl blur-2xl opacity-60 animate-pulse-slow" />

          {/* Main robot body */}
          <div className="relative w-full h-full bg-gradient-to-br from-indigo-500 via-purple-600 to-purple-700 rounded-3xl shadow-2xl backdrop-blur-xl border border-white/20 overflow-hidden">
            {imageUrl ? (
              <>
                {/* Custom Image as Main Body */}
                <img
                  src={imageUrl}
                  alt="AI Agent"
                  className="absolute inset-0 w-full h-full object-cover rounded-3xl"
                />
              </>
            ) : (
              <>
                {/* Default Robot Design */}
                {/* Glassmorphism overlay */}
                <div className="absolute inset-0 bg-white/10 backdrop-blur-sm" />

                {/* Top highlight */}
                <div className="absolute top-0 left-0 right-0 h-20 bg-gradient-to-b from-white/30 to-transparent rounded-t-3xl" />

                {/* Robot face container */}
                <div className="relative w-full h-full flex items-center justify-center">
                  {/* Eyes container */}
                  <div className="relative">
                    {/* Left eye */}
                    <div className="absolute -left-8 top-0 w-6 h-6 bg-white rounded-full shadow-lg animate-blink">
                      <div className="absolute inset-1 bg-gradient-to-br from-indigo-400 to-purple-600 rounded-full">
                        <div className="absolute top-1 left-1 w-2 h-2 bg-white rounded-full animate-pulse" />
                      </div>
                    </div>

                    {/* Right eye */}
                    <div className="absolute -right-8 top-0 w-6 h-6 bg-white rounded-full shadow-lg animate-blink-delayed">
                      <div className="absolute inset-1 bg-gradient-to-br from-indigo-400 to-purple-600 rounded-full">
                        <div className="absolute top-1 left-1 w-2 h-2 bg-white rounded-full animate-pulse" />
                      </div>
                    </div>

                    {/* Center icon */}
                    <div className="relative">
                      <div className="w-20 h-20 bg-white/20 rounded-full backdrop-blur-sm border-2 border-white/30 flex items-center justify-center overflow-hidden shadow-2xl">
                        <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M4 12h.01M4 8h.01M4 16h.01" />
                        </svg>
                      </div>
                      {/* Floating task indicators */}
                      <div className="absolute -top-2 -right-2 w-4 h-4 bg-green-400 rounded-full animate-ping" />
                      <div className="absolute -bottom-2 -left-2 w-4 h-4 bg-blue-400 rounded-full animate-ping" style={{ animationDelay: '1s' }} />
                    </div>
                  </div>

                  {/* Antenna */}
                  <div className="absolute -top-8 left-1/2 -translate-x-1/2">
                    <div className="w-1 h-8 bg-gradient-to-t from-purple-400 to-transparent" />
                    <div className="absolute -top-1 left-1/2 -translate-x-1/2 w-3 h-3 bg-pink-400 rounded-full animate-ping" />
                    <div className="absolute -top-1 left-1/2 -translate-x-1/2 w-3 h-3 bg-pink-500 rounded-full" />
                  </div>
                </div>

                {/* Bottom accent line */}
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-white/50 to-transparent" />
              </>
            )}
          </div>
        </div>

        {/* Floating rings around robot */}
        <div className="absolute inset-0 flex items-center justify-center animate-spin-slow">
          <div className="w-40 h-40 sm:w-48 sm:h-48 md:w-56 md:h-56 lg:w-64 lg:h-64 rounded-full border-4 border-indigo-400/20" />
        </div>
        <div className="absolute inset-0 flex items-center justify-center animate-spin-reverse">
          <div className="w-44 h-44 sm:w-52 sm:h-52 md:w-60 md:h-60 lg:w-68 lg:h-68 rounded-full border-2 border-purple-400/20" />
        </div>
      </div>

      {/* Bottom sparkles */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex gap-2">
        <div className="w-1 h-1 bg-indigo-400 rounded-full animate-twinkle-1" />
        <div className="w-1 h-1 bg-purple-400 rounded-full animate-twinkle-2" />
        <div className="w-1 h-1 bg-pink-400 rounded-full animate-twinkle-3" />
      </div>
    </div>
  );
}
