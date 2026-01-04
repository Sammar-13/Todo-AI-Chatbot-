"use client";

import React, { useState, useEffect } from "react";

interface SidebarRobotProps {
  username?: string;
}

export default function SidebarRobot({ username }: SidebarRobotProps) {
  const [showBubble, setShowBubble] = useState(false);

  useEffect(() => {
    // Show welcome message on mount (when user logs in/loads page)
    const timer = setTimeout(() => {
      setShowBubble(true);
      // Hide after 5 seconds
      const hideTimer = setTimeout(() => setShowBubble(false), 5000);
      return () => clearTimeout(hideTimer);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div 
      className="relative flex flex-col items-center justify-center w-full py-10 group cursor-pointer"
      onMouseEnter={() => setShowBubble(true)}
      onMouseLeave={() => setShowBubble(false)}
    >
      {/* Glow Effect behind robot */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-32 h-32 bg-indigo-500/10 rounded-full blur-3xl animate-glow pointer-events-none"></div>

      {/* Floating Robot Container - Slower and larger float for sidebar effect */}
      <div className="relative w-28 h-28 animate-float transition-transform duration-500 group-hover:scale-110">
        <svg
          viewBox="0 0 200 200"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="w-full h-full drop-shadow-[0_15px_15px_rgba(0,0,0,0.4)]"
        >
          {/* Antennas */}
          <line x1="100" y1="50" x2="100" y2="30" stroke="#6366f1" strokeWidth="4" />
          <circle cx="100" cy="30" r="5" fill="#a5b4fc" className="animate-pulse" />

          {/* Head */}
          <rect
            x="60"
            y="50"
            width="80"
            height="70"
            rx="20"
            fill="#1e293b"
            stroke="#475569"
            strokeWidth="2"
          />
          
          {/* Face Screen */}
          <rect
            x="70"
            y="65"
            width="60"
            height="40"
            rx="12"
            fill="#0f172a"
          />

          {/* Eyes Container (Blinking) */}
          <g className="animate-blink">
            {/* Left Eye */}
            <circle cx="85" cy="85" r="6" fill="#6366f1">
              <animate
                attributeName="opacity"
                values="0.6;1;0.6"
                dur="2s"
                repeatCount="indefinite"
              />
            </circle>
            {/* Right Eye */}
            <circle cx="115" cy="85" r="6" fill="#6366f1">
              <animate
                attributeName="opacity"
                values="0.6;1;0.6"
                dur="2s"
                repeatCount="indefinite"
              />
            </circle>
          </g>

          {/* Body */}
          <path
            d="M70 130 C70 125, 130 125, 130 130 L120 170 C120 180, 80 180, 80 170 Z"
            fill="#1e293b"
            stroke="#475569"
            strokeWidth="2"
          />
          
          {/* Chest Detail */}
          <circle cx="100" cy="150" r="8" fill="#334155" />
          <circle cx="100" cy="150" r="4" fill="#6366f1" className="animate-pulse" />

          {/* Floating Hands */}
          <circle cx="50" cy="150" r="10" fill="#1e293b" stroke="#475569" strokeWidth="2">
             <animate attributeName="cy" values="150;155;150" dur="3s" repeatCount="indefinite" />
          </circle>
          <circle cx="150" cy="150" r="10" fill="#1e293b" stroke="#475569" strokeWidth="2">
            <animate attributeName="cy" values="150;145;150" dur="3s" repeatCount="indefinite" />
          </circle>

          {/* Shadow */}
          <ellipse cx="100" cy="190" rx="30" ry="5" fill="#000000" opacity="0.3">
            <animate attributeName="rx" values="30;20;30" dur="4s" repeatCount="indefinite" />
            <animate attributeName="opacity" values="0.3;0.1;0.3" dur="4s" repeatCount="indefinite" />
          </ellipse>
        </svg>
      </div>

      {/* Chat Bubble - Positioned above robot */}
      <div 
        className={`absolute -top-10 left-1/2 -translate-x-1/2 w-48 transition-all duration-500 transform ${
          showBubble ? "opacity-100 translate-y-0 scale-100" : "opacity-0 translate-y-4 scale-90 pointer-events-none"
        }`}
      >
        <div className="bg-indigo-600 text-white text-xs px-4 py-2.5 rounded-2xl shadow-2xl relative font-bold text-center border border-indigo-400/30 backdrop-blur-sm">
          Hey {username || "Friend"}, <br /> glad to have you here! ❤️
          {/* Arrow */}
          <div className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-3 h-3 bg-indigo-600 rotate-45 border-r border-b border-indigo-400/30"></div>
        </div>
      </div>
    </div>
  );
}