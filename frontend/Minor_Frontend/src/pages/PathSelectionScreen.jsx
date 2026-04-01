import React from "react";
import { Brain, BarChart3, Zap } from "lucide-react";

export default function PathSelectionScreen({ file, onSelectPath }) {
  return (
    <div className="p-8 max-w-5xl mx-auto animate-fadeIn">
      <div className="mb-10 text-center">
        <h1 className="text-4xl font-black text-slate-800 mb-3">
          Analysis Mode Selection
        </h1>
        <p className="text-slate-500">
          Choose your analysis workflow for{" "}
          <span className="font-semibold text-slate-700">{file}</span>
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-3xl mx-auto">
        {/* Classification Only Path */}
        <button
          onClick={() => onSelectPath("classification")}
          className="group relative overflow-hidden rounded-2xl bg-gradient-to-br from-purple-500 to-indigo-600 p-8 shadow-lg transition-all hover:shadow-2xl hover:scale-105 active:scale-95"
        >
          <div className="absolute inset-0 bg-white/10 group-hover:bg-white/20 transition-all" />
          <div className="relative z-10">
            <div className="mb-4 flex justify-center">
              <div className="rounded-full bg-white/20 p-4 backdrop-blur-sm">
                <Brain className="h-10 w-10 text-white" />
              </div>
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">
              Classification
            </h2>
            <p className="text-white/90 text-sm mb-4">
              Fast tumor classification with confidence scores
            </p>
            <div className="space-y-2 text-left text-white/80 text-xs">
              <div className="flex items-center gap-2">
                <Zap className="h-4 w-4" />
                Instant results
              </div>
              <div className="flex items-center gap-2">
                <Zap className="h-4 w-4" />
                Confidence scores
              </div>
              <div className="flex items-center gap-2">
                <Zap className="h-4 w-4" />
                Probability distribution
              </div>
            </div>
            <div className="mt-6 inline-block rounded-lg bg-white/20 px-4 py-2 font-semibold text-white text-sm group-hover:bg-white/30 transition-all">
              Start Classification →
            </div>
          </div>
        </button>

        {/* Full Analysis Path */}
        <button
          onClick={() => onSelectPath("detection")}
          className="group relative overflow-hidden rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 p-8 shadow-lg transition-all hover:shadow-2xl hover:scale-105 active:scale-95"
        >
          <div className="absolute inset-0 bg-white/10 group-hover:bg-white/20 transition-all" />
          <div className="relative z-10">
            <div className="mb-4 flex justify-center">
              <div className="rounded-full bg-white/20 p-4 backdrop-blur-sm">
                <BarChart3 className="h-10 w-10 text-white" />
              </div>
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">
              Full Analysis
            </h2>
            <p className="text-white/90 text-sm mb-4">
              Complete pipeline with detection, segmentation & analytics
            </p>
            <div className="space-y-2 text-left text-white/80 text-xs">
              <div className="flex items-center gap-2">
                <Zap className="h-4 w-4" />
                Tumor detection
              </div>
              <div className="flex items-center gap-2">
                <Zap className="h-4 w-4" />
                Segmentation results
              </div>
              <div className="flex items-center gap-2">
                <Zap className="h-4 w-4" />
                Analytics dashboard
              </div>
            </div>
            <div className="mt-6 inline-block rounded-lg bg-white/20 px-4 py-2 font-semibold text-white text-sm group-hover:bg-white/30 transition-all">
              Start Full Analysis →
            </div>
          </div>
        </button>
      </div>

      <div className="mt-10 text-center text-slate-600 text-sm">
        <p>
          You can change your analysis mode at any time from the navigation menu
        </p>
      </div>
    </div>
  );
}
