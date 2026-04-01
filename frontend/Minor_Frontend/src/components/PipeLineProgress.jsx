import React from "react";
import {
  Upload,
  Search,
  FileText,
  Activity,
  Layers,
  BarChart3,
  CheckCircle2,
  ChevronRight,
} from "lucide-react";

export default function PipelineProgress({
  currentStage,
  onStageChange,
  workflowPath,
}) {
  // Classification workflow
  const classificationStages = [
    { id: "upload", label: "UPLOAD", icon: Upload },
    { id: "path-selection", label: "SELECT MODE", icon: Activity },
    { id: "classification", label: "CLASSIFICATION", icon: FileText },
    { id: "analytics", label: "ANALYTICS", icon: BarChart3 },
  ];

  // Detection & Full Analysis workflow
  const detectionStages = [
    { id: "upload", label: "UPLOAD", icon: Upload },
    { id: "path-selection", label: "SELECT MODE", icon: Activity },
    { id: "detection", label: "DETECTION", icon: Search },
    { id: "segmentation", label: "SEGMENTATION", icon: Layers },
    { id: "segmentation-analytics", label: "SEG ANALYSIS", icon: BarChart3 },
    { id: "analytics", label: "COMPLETE", icon: CheckCircle2 },
  ];

  // Choose stages based on workflow
  const stages =
    workflowPath === "classification" ? classificationStages : detectionStages;

  return (
    <div className="w-full max-w-7xl mx-auto px-4 mb-12">
      <div className="relative">
        {/* Stage Circles and Arrows */}
        <div className="flex items-center justify-between">
          {stages.map((stage, index) => {
            const stageIndex = stages.findIndex((s) => s.id === stage.id);
            const currentIndex = stages.findIndex((s) => s.id === currentStage);
            const isActive = stage.id === currentStage;
            const isPast = currentIndex > stageIndex;
            const isFuture = currentIndex < stageIndex;

            return (
              <React.Fragment key={stage.id}>
                <button
                  onClick={() => onStageChange?.(stage.id)}
                  className="flex flex-col items-center gap-2 group focus:outline-none transition-all"
                >
                  <div
                    className={`w-14 h-14 rounded-full border-2.5 flex items-center justify-center transition-all transform ${
                      isActive
                        ? "border-cyan-500 bg-gradient-to-br from-cyan-50 to-blue-50 ring-4 ring-cyan-200 shadow-lg scale-110"
                        : isPast
                          ? "border-green-500 bg-gradient-to-br from-green-50 to-emerald-50 shadow-md"
                          : "border-gray-300 bg-white hover:border-cyan-300 hover:shadow-md"
                    } cursor-pointer`}
                  >
                    <stage.icon
                      size={24}
                      className={`transition-colors ${
                        isActive || isPast
                          ? "text-cyan-600"
                          : "text-gray-400 group-hover:text-cyan-500"
                      }`}
                    />
                  </div>
                  <div className="text-center">
                    <p
                      className={`text-xs font-bold tracking-wider transition-colors ${
                        isActive
                          ? "text-cyan-600"
                          : isPast
                            ? "text-green-600"
                            : "text-gray-400 group-hover:text-cyan-500"
                      }`}
                    >
                      {stage.label}
                    </p>
                    {isPast && (
                      <p className="text-xs text-green-500 font-semibold">
                        Done
                      </p>
                    )}
                  </div>
                </button>

                {/* Arrow between stages */}
                {index < stages.length - 1 && (
                  <div
                    className={`flex-1 flex justify-center transition-all duration-300 ${
                      currentIndex > stageIndex ? "opacity-100" : "opacity-50"
                    }`}
                  >
                    <ChevronRight
                      size={24}
                      className={`transition-colors ${
                        currentIndex > stageIndex
                          ? "text-blue-500"
                          : currentIndex === stageIndex
                            ? "text-cyan-400 animate-pulse"
                            : "text-gray-300"
                      }`}
                    />
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </div>
  );
}
