import React from "react";
import { Activity, Layers, AlertCircle, Plus } from "lucide-react";

export default function ClassificationScreen({
  onNext,
  results,
  file,
  onNewAnalysis,
}) {
  if (!results) {
    return (
      <div className="p-8 max-w-6xl mx-auto">
        <div className="text-center p-12 bg-yellow-50 border border-yellow-200 rounded-lg">
          <AlertCircle className="text-yellow-600 mx-auto mb-4" size={48} />
          <p className="text-yellow-800 font-semibold">
            No classification results available
          </p>
          <p className="text-yellow-700 text-sm mt-2">
            Please upload an image first
          </p>
        </div>
      </div>
    );
  }

  const tumorType = results?.result || "Unknown";

  const confidence = results?.confidence
    ? (results.confidence * 100).toFixed(1)
    : "0.0";

  const allProbs =
    typeof results?.all_probabilities === "object"
      ? results.all_probabilities
      : {};

  return (
    <div className="p-8 max-w-6xl mx-auto grid grid-cols-12 gap-8 animate-fadeIn">
      <div className="col-span-12 flex justify-between items-end mb-2">
        <div>
          <span className="text-xs font-bold text-rose-500 uppercase tracking-widest">
            Classification Phase
          </span>
          <h2 className="text-3xl font-black text-slate-800">
            Classification Report
          </h2>
        </div>
        <div className="flex items-center gap-3">
          <p className="text-sm font-mono font-bold text-slate-600 bg-white px-3 py-1 rounded-md border">
            File: {file}
          </p>
          {onNewAnalysis && (
            <button
              onClick={onNewAnalysis}
              className="flex items-center gap-2 bg-gradient-to-r from-green-500 to-emerald-600 text-white px-4 py-2 rounded-lg text-sm font-bold shadow-md hover:shadow-lg hover:scale-105 transition-all active:scale-95"
            >
              <Plus size={16} /> New Analysis
            </button>
          )}
        </div>
      </div>

      <div className="col-span-8 bg-slate-900 rounded-3xl p-6 relative overflow-hidden h-[550px] flex items-center justify-center shadow-xl">
        <div className="absolute top-6 left-6 text-cyan-400 text-xs font-mono leading-relaxed opacity-80">
          Classification Model
          <br />
          ResNet-101 Backbone
          <br />
          Multi-Head Attention
        </div>

        {/* Result Visualization */}
        <div className="w-96 h-96 rounded-full bg-gradient-to-tr from-slate-800 to-slate-700 border border-slate-600 flex items-center justify-center relative">
          <div className="absolute w-full h-px bg-cyan-500/30" />
          <div className="absolute h-full w-px bg-cyan-500/30" />
          <div className="text-center">
            <Activity className="text-cyan-500/40 mx-auto mb-4" size={80} />
            <p className="text-cyan-400 text-sm font-bold">Analysis Complete</p>
          </div>
        </div>

        <div className="absolute bottom-6 left-6 text-white text-sm font-bold bg-black/50 px-4 py-2 rounded-lg backdrop-blur-sm">
          Model: Classification v1.0
        </div>
      </div>

      <div className="col-span-4 flex flex-col gap-6">
        <div className="bg-white border-2 border-slate-100 rounded-3xl p-8 shadow-sm border-l-8 border-l-cyan-400 flex-1">
          <div className="flex justify-between items-start mb-6">
            <span className="bg-cyan-50 text-cyan-600 text-xs font-bold px-3 py-1.5 rounded-md">
              High Confidence Result
            </span>
            <span className="text-xs font-bold text-slate-400">
              ID: CLS-{Math.random().toString(36).substr(2, 9).toUpperCase()}
            </span>
          </div>
          <h3 className="text-4xl font-black text-cyan-400 leading-tight mb-4 uppercase">
            {tumorType}
            <br />
            Detected
          </h3>
          <p className="text-sm text-slate-600 mb-8 font-medium">
            Pathological features consistent with detected tumor type
            classification.
          </p>

          <div className="flex items-center gap-4 bg-slate-50 p-4 rounded-xl border border-slate-100 mb-6">
            <div className="text-5xl font-black text-slate-800">
              {confidence}
              <span className="text-2xl text-slate-400">%</span>
            </div>
            <div className="text-[10px] font-bold text-slate-500 leading-tight tracking-wider uppercase">
              Confidence Score
              <br />
              Model Certainty Level
            </div>
          </div>

          <div className="space-y-2 mb-6">
            <p className="text-xs font-bold text-slate-500 uppercase">
              All Probabilities
            </p>
            {Object.entries(allProbs).map(([label, prob]) => (
              <div key={label} className="flex items-center justify-between">
                <span className="text-xs text-slate-600">{label}</span>
                <div className="flex items-center gap-2 flex-1 ml-2">
                  <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-cyan-400 to-blue-500 transition-all"
                      style={{ inlineSize: `${prob * 100}%` }}
                    />
                  </div>
                  <span className="text-xs font-bold text-slate-600 w-12 text-right">
                    {(prob * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white border border-slate-100 rounded-3xl p-6 shadow-sm">
          <h4 className="text-xs font-bold text-cyan-500 uppercase tracking-widest mb-4 flex items-center gap-2">
            <Layers size={16} /> Model Information
          </h4>
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div>
              <p className="text-[10px] text-slate-400 font-bold uppercase mb-1">
                Backbone
              </p>
              <p className="text-sm font-bold text-slate-700">ResNet-101</p>
            </div>
            <div>
              <p className="text-[10px] text-slate-400 font-bold uppercase mb-1">
                Attention
              </p>
              <p className="text-sm font-bold text-slate-700">
                Multi-Head Spatial
              </p>
            </div>
          </div>
          <div className="space-y-3">
            {onNewAnalysis && (
              <button
                onClick={onNewAnalysis}
                className="w-full bg-gradient-to-r from-green-500 to-emerald-600 text-white py-3.5 rounded-xl font-bold text-sm hover:shadow-lg transition-all shadow-md active:scale-95 flex items-center justify-center gap-2"
              >
                <Plus size={16} /> Start New Analysis
              </button>
            )}
            <button
              onClick={onNext}
              className="w-full bg-slate-900 text-white py-3.5 rounded-xl font-bold text-sm hover:bg-cyan-500 transition-colors shadow-lg shadow-slate-900/20"
            >
              Upload Another Image
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
