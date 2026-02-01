import Link from "next/link";
import AnimatedRobot from "@/components/AnimatedRobot";

export default function Home() {
  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-50 via-white to-purple-50" />

      {/* Floating shapes */}
      <div className="absolute top-20 left-10 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-float" />
      <div className="absolute top-40 right-10 w-72 h-72 bg-indigo-300 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-float-delayed" />
      <div className="absolute bottom-20 left-1/3 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-float" />

      {/* Content */}
      <div className="relative">
        {/* Navbar */}
        <nav className="px-6 py-4">
          <div className="max-w-6xl mx-auto flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <span className="text-xl font-bold text-gray-900">TaskFlow</span>
            </div>
            <div className="flex items-center gap-4">
              <Link href="/signin" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors">
                Sign In
              </Link>
              <Link href="/signup" className="btn-primary">
                Get Started
              </Link>
            </div>
          </div>
        </nav>

        {/* Hero */}
        <section className="px-4 sm:px-6 py-12 sm:py-16 md:py-20 lg:py-32">
          <div className="max-w-7xl mx-auto">
            <div className="grid lg:grid-cols-2 gap-8 md:gap-10 lg:gap-12 items-center">
              {/* Left Column - Content */}
              <div className="space-y-4 sm:space-y-6 md:space-y-8">
                <div className="inline-flex items-center gap-2 px-3 py-1.5 sm:px-4 sm:py-2 rounded-full bg-indigo-100 text-indigo-700 text-xs sm:text-sm font-medium">
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
                  </span>
                  Powered by AI Assistant
                </div>

                <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-bold text-gray-900 leading-tight">
                  Organize your life with{" "}
                  <span className="gradient-text">TaskFlow</span>
                </h1>

                <p className="text-base sm:text-lg md:text-xl text-gray-600 max-w-xl">
                  Your personal AI agent that plans, creates, updates, and completes tasks for you — so you can focus on what truly matters.
                </p>

                <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
                  <Link href="/signup" className="btn-primary text-sm sm:text-base px-6 sm:px-8 py-3 sm:py-4 inline-flex items-center justify-center">
                    <svg className="w-4 h-4 sm:w-5 sm:h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    Start Free Today
                  </Link>
                  <Link href="/signin" className="btn-secondary text-sm sm:text-base px-6 sm:px-8 py-3 sm:py-4 inline-flex items-center justify-center">
                    I already have an account
                  </Link>
                </div>

                {/* Feature highlights */}
                <div className="flex flex-wrap gap-4 sm:gap-6 pt-2 sm:pt-4">
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 sm:w-5 sm:h-5 rounded-full bg-green-500 flex items-center justify-center">
                      <svg className="w-2.5 h-2.5 sm:w-3 sm:h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <span className="text-xs sm:text-sm text-gray-600 font-medium">AI-Powered</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 sm:w-5 sm:h-5 rounded-full bg-blue-500 flex items-center justify-center">
                      <svg className="w-2.5 h-2.5 sm:w-3 sm:h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <span className="text-xs sm:text-sm text-gray-600 font-medium">Free Forever</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 sm:w-5 sm:h-5 rounded-full bg-purple-500 flex items-center justify-center">
                      <svg className="w-2.5 h-2.5 sm:w-3 sm:h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <span className="text-xs sm:text-sm text-gray-600 font-medium">No Credit Card</span>
                  </div>
                </div>
              </div>

              {/* Right Column - Animated Robot */}
              <div className="relative order-first lg:order-last">
                <AnimatedRobot imageUrl="https://files.imagetourl.net/uploads/1768181349281-86e76f6a-e3fe-457e-b8c0-b30df1d1e02b.png" />

                <div className="mt-4 sm:mt-6 md:mt-8 text-center lg:text-left">
                  <p className="text-base sm:text-lg text-gray-700 font-medium">Meet Your AI-Powered Task Assistant</p>
                  <p className="text-xs sm:text-sm text-gray-500">Create • Organize • Complete • Automate</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section - AI Focused */}
        <section className="px-6 py-20 bg-gradient-to-b from-white/50 to-indigo-50/30">
          <div className="max-w-7xl mx-auto">
            {/* Section Header */}
            <div className="text-center mb-16">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-100 text-indigo-700 text-sm font-medium mb-6">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
                </span>
                AI-Powered Features
              </div>
              <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
                Your AI Agent Does the{" "}
                <span className="gradient-text">Heavy Lifting</span>
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Experience the future of task management with an intelligent AI assistant that understands you
              </p>
            </div>

            {/* Features Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {/* Feature 1: AI Task Management */}
              <div className="group relative bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-gray-100 overflow-hidden">
                {/* Gradient overlay on hover */}
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

                <div className="relative z-10">
                  {/* Icon */}
                  <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>

                  {/* Content */}
                  <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-indigo-600 transition-colors">
                    AI Task Management
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    Just tell your AI agent to add, edit, or delete tasks — it does it instantly.
                  </p>

                  {/* Decorative element */}
                  <div className="absolute top-4 right-4 w-20 h-20 bg-indigo-100 rounded-full blur-2xl opacity-0 group-hover:opacity-50 transition-opacity duration-300" />
                </div>
              </div>

              {/* Feature 2: Track Progress */}
              <div className="group relative bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-gray-100 overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 to-teal-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

                <div className="relative z-10">
                  <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>

                  <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-emerald-600 transition-colors">
                    Auto Track Progress
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    AI agent keeps your tasks updated and marks them complete automatically.
                  </p>

                  <div className="absolute top-4 right-4 w-20 h-20 bg-emerald-100 rounded-full blur-2xl opacity-0 group-hover:opacity-50 transition-opacity duration-300" />
                </div>
              </div>

              {/* Feature 3: Quick Task Creation */}
              <div className="group relative bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-gray-100 overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-cyan-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

                <div className="relative z-10">
                  <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-600 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>

                  <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-blue-600 transition-colors">
                    Lightning Fast
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    Speak or type your task and your AI agent adds it in seconds.
                  </p>

                  <div className="absolute top-4 right-4 w-20 h-20 bg-blue-100 rounded-full blur-2xl opacity-0 group-hover:opacity-50 transition-opacity duration-300" />
                </div>
              </div>

              {/* Feature 4: Smart Automation */}
              <div className="group relative bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-gray-100 overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-orange-500/5 to-pink-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

                <div className="relative z-10">
                  <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-orange-500 to-pink-600 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                    </svg>
                  </div>

                  <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-orange-600 transition-colors">
                    Smart Automation
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    AI learns your patterns and suggests tasks, priorities, and optimal schedules.
                  </p>

                  <div className="absolute top-4 right-4 w-20 h-20 bg-orange-100 rounded-full blur-2xl opacity-0 group-hover:opacity-50 transition-opacity duration-300" />
                </div>
              </div>
            </div>

            {/* Bottom CTA */}
            <div className="text-center mt-16">
              <p className="text-gray-600 mb-6">
                Experience the power of AI-driven task management
              </p>
              <Link href="/signup" className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-xl hover:from-indigo-700 hover:to-purple-700 transition-all duration-200 shadow-lg hover:shadow-xl">
                Try AI Agent Free
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </Link>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="px-6 py-20">
          <div className="max-w-4xl mx-auto">
            <div className="card p-12 text-center bg-gradient-to-br from-indigo-600 to-purple-700">
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                Ready to get organized?
              </h2>
              <p className="text-lg text-indigo-100 mb-8 max-w-xl mx-auto">
                Join thousands of users who have simplified their task management with TaskFlow.
              </p>
              <Link href="/signup" className="inline-flex items-center justify-center px-8 py-4 text-base font-semibold rounded-xl text-indigo-600 bg-white hover:bg-gray-100 transition-all duration-200 shadow-lg">
                Create Free Account
                <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </Link>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
