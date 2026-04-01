import React from "react";
import {
  Search,
  CheckCircle2,
  XCircle,
  AlertCircle,
  MapPin,
} from "lucide-react";

export default function DetectionScreen({ onNext, results, file }) {
  if (!results) {
    return (
      <div className="p-8 max-w-6xl mx-auto">
        <div className="text-center p-12 bg-yellow-50 border border-yellow-200 rounded-lg">
          <AlertCircle className="text-yellow-600 mx-auto mb-4" size={48} />
          <p className="text-yellow-800 font-semibold">
            No detection results available
          </p>
          <p className="text-yellow-700 text-sm mt-2">
            Please upload an image first
          </p>
        </div>
      </div>
    );
  }

  const detections = results.detections || [];
  const tumorCount = results.tumor_count || 0;

  // Calculate tumor statistics
  const avgConfidence =
    detections.length > 0
      ? (
          (detections.reduce((sum, det) => sum + det.confidence, 0) /
            detections.length) *
          100
        ).toFixed(1)
      : 0;

  const totalArea = detections.reduce((sum, det) => sum + (det.area || 0), 0);

  return (
    <div className="p-8 max-w-6xl mx-auto grid grid-cols-12 gap-8 animate-fadeIn">
      <div className="col-span-8">
        <div className="mb-4">
          <h2 className="text-3xl font-black text-slate-800">
            Lesion Detection
          </h2>
          <p className="text-slate-500 text-sm font-medium">
            Identifying ROI via YOLO Detection Model - File: {file}
          </p>
        </div>

        <div className="bg-slate-900 rounded-3xl h-[500px] relative overflow-hidden flex items-center justify-center">
          {results.detected_image && (
            <img
              src={`data:image/png;base64,${results.detected_image}`}
              alt="Detection Result"
              className="w-100% h-full object-contain"
            />
          )}
          {!results.detected_image && (
            <div className="text-center">
              <Search className="text-cyan-500/30 mx-auto mb-4" size={100} />
              <p className="text-cyan-400 text-sm font-bold">
                Detection visualization
              </p>
            </div>
          )}
          <div className="absolute top-4 left-4 flex gap-2">
            <span className="bg-cyan-500 text-white text-[10px] font-bold px-2 py-1 rounded">
              TUMOR DETECTED
            </span>
            <span className="bg-blue-500 text-white text-[10px] font-bold px-2 py-1 rounded">
              YOLO v8
            </span>
          </div>
        </div>
      </div>

      <div className="col-span-4 flex flex-col">
        <div className="bg-white border rounded-3xl p-6 mb-4 shadow-sm">
          <h3 className="font-bold text-sm text-slate-800 mb-4 uppercase tracking-wider">
            Detection Summary
          </h3>
          <div className="space-y-3">
            <div className="p-3 bg-cyan-50 rounded-lg border border-cyan-200">
              <p className="text-xs text-cyan-600 font-bold uppercase">
                Tumor Count
              </p>
              <p className="text-2xl font-black text-cyan-600">{tumorCount}</p>
            </div>
            <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
              <p className="text-xs text-blue-600 font-bold uppercase">
                Avg Confidence
              </p>
              <p className="text-lg font-bold text-blue-600">
                {avgConfidence}%
              </p>
            </div>
            <div className="p-3 bg-purple-50 rounded-lg border border-purple-200">
              <p className="text-xs text-purple-600 font-bold uppercase">
                Total Area
              </p>
              <p className="text-lg font-bold text-purple-600">
                {(totalArea / 1000).toFixed(1)}k px²
              </p>
            </div>
            <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
              <p className="text-xs text-blue-600 font-bold uppercase">Model</p>
              <p className="text-sm font-bold text-blue-600">YOLO v8 MED</p>
            </div>
          </div>
        </div>

        <div className="bg-white border rounded-3xl p-6 flex-1 shadow-sm overflow-y-auto">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-bold text-sm text-slate-800 uppercase tracking-wider">
              Detected Regions ({detections.length})
            </h3>
            <button className="text-[10px] font-bold text-cyan-500 hover:underline">
              RESET ALL
            </button>
          </div>

          {detections.length === 0 ? (
            <div className="text-center py-8">
              <Search className="text-slate-300 mx-auto mb-2" size={40} />
              <p className="text-slate-500 text-sm">No detections found</p>
            </div>
          ) : (
            <div className="space-y-4">
              {detections.map((det, i) => (
                <div
                  key={i}
                  className="border border-slate-100 bg-slate-50 p-4 rounded-2xl hover:border-cyan-400 transition-colors"
                >
                  <div className="flex justify-between items-start mb-3">
                    <span className="font-bold text-sm text-slate-700">
                      • Detection {i + 1}
                    </span>
                    <span className="text-xs font-bold text-cyan-500 bg-cyan-100 px-2 py-1 rounded">
                      {(det.confidence * 100).toFixed(1)}% Conf.
                    </span>
                  </div>

                  {/* Coordinates Section */}
                  <div className="mb-4">
                    <p className="text-xs font-bold text-slate-600 mb-2 flex items-center gap-1">
                      <MapPin size={12} /> Tumor Location (pixels)
                    </p>
                    <div className="bg-white border border-slate-200 rounded-lg p-3 space-y-2 text-xs font-mono">
                      <div className="grid grid-cols-2 gap-2">
                        <div className="bg-cyan-50 p-2 rounded">
                          <span className="text-slate-500">X1:</span>
                          <p className="font-bold text-slate-700">
                            {det.bbox[0]}
                          </p>
                        </div>
                        <div className="bg-cyan-50 p-2 rounded">
                          <span className="text-slate-500">X2:</span>
                          <p className="font-bold text-slate-700">
                            {det.bbox[2]}
                          </p>
                        </div>
                      </div>
                      <div className="grid grid-cols-2 gap-2">
                        <div className="bg-blue-50 p-2 rounded">
                          <span className="text-slate-500">Y1:</span>
                          <p className="font-bold text-slate-700">
                            {det.bbox[1]}
                          </p>
                        </div>
                        <div className="bg-blue-50 p-2 rounded">
                          <span className="text-slate-500">Y2:</span>
                          <p className="font-bold text-slate-700">
                            {det.bbox[3]}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Center Point */}
                  <div className="mb-4">
                    <p className="text-xs font-bold text-slate-600 mb-2">
                      Center Point
                    </p>
                    <div className="bg-purple-50 border border-purple-200 rounded-lg p-2 text-xs font-mono">
                      <span className="text-slate-600">Center: </span>
                      <span className="font-bold text-purple-600">
                        ({Math.round((det.bbox[0] + det.bbox[2]) / 2)},{" "}
                        {Math.round((det.bbox[1] + det.bbox[3]) / 2)})
                      </span>
                    </div>
                  </div>

                  {/* Dimensions */}
                  {det.area && (
                    <div className="mb-4">
                      <p className="text-xs font-bold text-slate-600 mb-2">
                        Dimensions
                      </p>
                      <div className="bg-orange-50 border border-orange-200 rounded-lg p-2 text-xs">
                        <p>
                          Width:{" "}
                          <span className="font-bold">
                            {det.bbox[2] - det.bbox[0]}px
                          </span>
                        </p>
                        <p>
                          Height:{" "}
                          <span className="font-bold">
                            {det.bbox[3] - det.bbox[1]}px
                          </span>
                        </p>
                        <p>
                          Area:{" "}
                          <span className="font-bold">
                            {det.area.toLocaleString()}px²
                          </span>
                        </p>
                      </div>
                    </div>
                  )}

                  {/* Action Buttons */}
                  <div className="flex gap-2">
                    <button className="flex-1 flex items-center justify-center gap-1 bg-cyan-500 text-white py-2 rounded-lg text-xs font-bold hover:bg-cyan-600">
                      <CheckCircle2 size={14} /> Accept
                    </button>
                    <button className="flex-1 flex items-center justify-center gap-1 bg-white border border-slate-200 text-slate-600 py-2 rounded-lg text-xs font-bold hover:bg-slate-50">
                      <XCircle size={14} /> Reject
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
          <button
            onClick={onNext}
            className="w-full mt-6 bg-slate-900 text-white py-3.5 rounded-xl font-bold text-sm hover:bg-cyan-500 transition-colors"
          >
            Proceed to Segmentation
          </button>
        </div>
      </div>
    </div>
  );
}
