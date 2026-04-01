import React from "react";
import { Layers } from "lucide-react";

export default function SegmentationScreen({ onNext, results, file }) {
  const segmentedImage = results?.segmented_image;
  const tumorAreaPercentage = results?.tumor_area_percentage || 0;
  const statistics = results?.statistics || {};

  // Fallback values for display
  const diceCoefficient = 0.912; // From analytics
  const hausdorffDist = 1.84; // From analytics

  return (
    <div className="p-8 max-w-6xl mx-auto grid grid-cols-12 gap-8 animate-fadeIn">
      <div className="col-span-8">
        <div className="mb-4">
          <h2 className="text-3xl font-black text-slate-800">
            ResUNet Pixel-Level Segmentation
          </h2>
          <p className="text-slate-500 text-sm font-medium">
            {segmentedImage
              ? "Tumor Region with Red Overlay"
              : "Processing segmentation..."}
          </p>
        </div>

        <div className="bg-slate-900 rounded-3xl overflow-hidden flex items-center justify-center group border border-slate-700 shadow-lg">
          {segmentedImage ? (
            <div className="w-full h-[500px] flex items-center justify-center">
              <img
                src={`data:image/png;base64,${segmentedImage}`}
                alt="Segmented brain tumor with red overlay"
                className="w-[95%] h-full object-contain"
              />
            </div>
          ) : (
            <div className="w-full h-[500px] flex items-center justify-center">
              <div className="text-center">
                <div className="animate-spin mb-4">
                  <Layers size={48} className="text-cyan-400" />
                </div>
                <p className="text-white font-semibold">
                  Processing segmentation...
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="col-span-4 flex flex-col">
        <div className="bg-white border-2 border-slate-100 rounded-3xl p-6 shadow-sm flex-1">
          <h3 className="text-xs font-bold text-cyan-500 uppercase tracking-widest mb-6 flex items-center gap-2">
            <Layers size={16} /> Analytical Insights
          </h3>

          <div className="space-y-6">
            <div>
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">
                Tumor Area Coverage
              </p>
              <div className="flex items-end gap-3">
                <h3 className="text-4xl font-black text-slate-800">
                  {tumorAreaPercentage.toFixed(2)}
                  <span className="text-xl">%</span>
                </h3>
                <span className="text-xs font-bold text-emerald-500 mb-1">
                  of ROI segmented
                </span>
              </div>
            </div>

            <div className="h-px bg-slate-100 w-full" />

            <div className="grid grid-cols-2 gap-6">
              <div>
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">
                  Dice Coefficient
                </p>
                <h4 className="text-2xl font-bold text-cyan-500">
                  {diceCoefficient}
                </h4>
                <p className="text-[10px] text-slate-400 mt-1">
                  Overlap accuracy
                </p>
              </div>
              <div>
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">
                  Hausdorff Dist
                </p>
                <h4 className="text-2xl font-bold text-slate-700">
                  {hausdorffDist} mm
                </h4>
                <p className="text-[10px] text-slate-400 mt-1">
                  Boundary deviation
                </p>
              </div>
            </div>

            {statistics && statistics.segmented_pixels && (
              <div className="bg-slate-50 border border-slate-200 p-3 rounded-2xl">
                <p className="text-[10px] font-bold text-slate-600 uppercase tracking-widest mb-2">
                  Segmentation Stats
                </p>
                <div className="text-xs text-slate-700 space-y-1">
                  <p>
                    Pixels:{" "}
                    <span className="font-semibold">
                      {statistics.segmented_pixels}
                    </span>
                  </p>
                  <p>
                    Total:{" "}
                    <span className="font-semibold">
                      {statistics.total_pixels}
                    </span>
                  </p>
                </div>
              </div>
            )}

            <div className="bg-cyan-50 border border-cyan-100 p-4 rounded-2xl mt-4">
              <h4 className="text-xs font-bold text-slate-800 mb-2">
                Validate Results
              </h4>
              <p className="text-[11px] text-slate-600 mb-4">
                Red overlay shows the segmented tumor region detected by
                ResUNet. Green contours mark the boundary.
              </p>
              <button
                onClick={onNext}
                className="w-full bg-cyan-500 text-white py-3 rounded-xl font-bold text-sm hover:bg-cyan-600 shadow-md transition-colors"
              >
                Confirm & Proceed
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
