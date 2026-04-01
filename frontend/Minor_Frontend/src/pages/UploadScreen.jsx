import React, { useState, useRef } from "react";
import { Upload, Layers, CheckCircle2, AlertCircle } from "lucide-react";
import { apiClient } from "../services/api";

export default function UploadScreen({ onNext, onAnalysisComplete }) {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const supportedFormats = [
    ".dcm",
    ".nii",
    ".nii.gz",
    ".jpg",
    ".jpeg",
    ".png",
    ".tif",
    ".tiff",
  ];

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const validateFiles = (files) => {
    const validFiles = [];
    let totalSize = 0;

    for (let file of files) {
      const fileExt = "." + file.name.split(".").pop().toLowerCase();
      const isSupported = supportedFormats.some(
        (fmt) => fileExt.endsWith(fmt) || file.name.endsWith(".nii.gz"),
      );

      if (!isSupported) {
        setError(
          `File ${file.name} is not supported. Please use DICOM, NIFTI, JPEG, PNG, or TIFF formats.`,
        );
        return [];
      }

      totalSize += file.size;
      if (totalSize > 256 * 1024 * 1024) {
        setError("Total file size exceeds 256MB limit.");
        return [];
      }

      validFiles.push(file);
    }

    setError(null);
    return validFiles;
  };

  const handleFiles = (files) => {
    const validFiles = validateFiles(files);
    if (validFiles.length > 0) {
      setUploadedFiles(validFiles);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    handleFiles(e.dataTransfer.files);
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e) => {
    handleFiles(e.target.files);
  };

  const handleProceed = async () => {
    if (uploadedFiles.length === 0 || uploading) return;

    setUploading(true);
    try {
      // Send first file to backend for analysis
      const file = uploadedFiles[0];

      // Call complete analysis endpoint to get all three results
      const results = await apiClient.analyze(file);

      // Store results in parent component
      onAnalysisComplete({
        file: file.name,
        classification: results.classification,
        detection: results.detection,
        segmentation: results.segmentation,
      });

      // Move to classification screen
      onNext();
    } catch (err) {
      setError(
        `Upload failed: ${err.message}. Make sure backend is running on http://localhost:8000`,
      );
      console.error("Upload error:", err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-8 max-w-5xl mx-auto animate-fadeIn">
      <div className="mb-10 text-center">
        <h1 className="text-4xl font-black text-slate-800 mb-3">
          MRI Data Ingestion
        </h1>
        <p className="text-slate-500">
          Upload diagnostic imaging to begin automated tumor classification and
          detection.
        </p>
      </div>

      <div
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-3xl p-24 flex flex-col items-center justify-center cursor-pointer transition-all group ${
          dragActive
            ? "border-cyan-500 bg-cyan-50 shadow-xl"
            : "border-cyan-200 bg-white hover:border-cyan-400 hover:shadow-xl"
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".dcm,.nii,.nii.gz,.jpg,.jpeg,.png,.tif,.tiff"
          onChange={handleFileChange}
          className="hidden"
        />

        <div className="bg-cyan-50 p-6 rounded-full mb-6 group-hover:scale-110 transition-transform">
          <Upload className="text-cyan-500" size={48} />
        </div>

        {!uploading && uploadedFiles.length === 0 && (
          <>
            <h3 className="text-2xl font-bold text-slate-700 mb-2">
              Drag and drop MRI studies here
            </h3>
            <p className="text-sm text-slate-400 max-w-md text-center leading-relaxed">
              Support for multiple DICOM series, NIFTI (.nii, .nii.gz), TIFF
              (.tif, .tiff), and high-resolution JPEG/PNG formats.
            </p>
          </>
        )}

        {uploading && (
          <div className="text-center">
            <div className="animate-spin mb-4">
              <Upload className="text-cyan-500" size={48} />
            </div>
            <h3 className="text-xl font-bold text-slate-700">
              Sending to analysis...
            </h3>
            <p className="text-sm text-slate-500 mt-2">
              Processing with Classification, Detection & Segmentation models
            </p>
          </div>
        )}

        {!uploading && uploadedFiles.length > 0 && (
          <div className="text-center">
            <CheckCircle2 className="text-green-500 mx-auto mb-4" size={48} />
            <h3 className="text-xl font-bold text-slate-700">
              {uploadedFiles.length} file{uploadedFiles.length !== 1 ? "s" : ""}{" "}
              ready
            </h3>
            <p className="text-sm text-slate-500 mt-2">
              {uploadedFiles.map((f) => f.name).join(", ")}
            </p>
          </div>
        )}

        <button
          onClick={handleBrowseClick}
          disabled={uploading}
          className="mt-8 px-8 py-3 bg-cyan-500 hover:bg-cyan-600 disabled:bg-cyan-300 text-white rounded-xl font-bold shadow-md transition-colors"
        >
          Browse Local Files
        </button>
        <button className="mt-4 text-cyan-600 font-bold text-sm flex items-center gap-2 hover:underline">
          <Layers size={16} /> PACS Integration
        </button>
      </div>

      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
          <AlertCircle
            className="text-red-500 flex-shrink-0 mt-0.5"
            size={20}
          />
          <p className="text-red-700 text-sm">{error}</p>
        </div>
      )}

      {uploadedFiles.length > 0 && !uploading && (
        <div className="mt-6 flex justify-center gap-4">
          <button
            onClick={handleBrowseClick}
            className="px-6 py-2 border border-cyan-500 text-cyan-600 rounded-lg font-semibold hover:bg-cyan-50 transition-colors"
          >
            Add More Files
          </button>
          <button
            onClick={handleProceed}
            className="px-8 py-2 bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg font-semibold shadow-md transition-colors"
          >
            Proceed to Classification
          </button>
        </div>
      )}

      <div className="mt-8 flex justify-between text-[11px] font-bold text-slate-400 tracking-widest uppercase px-4">
        <span>Maximum batch size: 256MB</span>
        <span className="flex gap-4">
          <span>End-to-End Encrypted</span>
          <span className="text-cyan-600">Average Processing: 45s</span>
        </span>
      </div>
    </div>
  );
}
