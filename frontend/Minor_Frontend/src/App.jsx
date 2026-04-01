import React, { useState } from "react";
import Navbar from "./components/Navbar";
import PipelineProgress from "./components/PipelineProgress";
import Footer from "./components/Footer";

// Pages
import UploadScreen from "./pages/UploadScreen";
import PathSelectionScreen from "./pages/PathSelectionScreen";
import ClassificationScreen from "./pages/ClassificationScreen";
import DetectionScreen from "./pages/DetectionScreen";
import SegmentationScreen from "./pages/SegmentationScreen";
import AnalyticsDashboard from "./pages/AnalyticDashboard";

export default function App() {
  const [stage, setStage] = useState("upload");
  const [workflowPath, setWorkflowPath] = useState(null); // "classification" or "detection"
  const [analysisResults, setAnalysisResults] = useState({
    file: null,
    classification: null,
    detection: null,
    segmentation: null,
  });

  const handleStageChange = (newStage) => {
    // Allow navigation to any stage
    setStage(newStage);
  };

  const handleAnalysisComplete = (results) => {
    setAnalysisResults(results);
  };

  const handlePathSelect = (path) => {
    setWorkflowPath(path);
    if (path === "classification") {
      setStage("classification");
    } else if (path === "detection") {
      setStage("detection");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-slate-50 font-sans text-slate-900">
      <Navbar setStage={setStage} workflowPath={workflowPath} />

      <main className="py-8">
        <PipelineProgress
          currentStage={stage}
          onStageChange={handleStageChange}
          workflowPath={workflowPath}
        />

        {stage === "upload" && (
          <UploadScreen
            onNext={() => setStage("path-selection")}
            onAnalysisComplete={handleAnalysisComplete}
          />
        )}

        {stage === "path-selection" && (
          <PathSelectionScreen
            file={analysisResults.file}
            onSelectPath={handlePathSelect}
          />
        )}

        {/* Classification Path */}
        {stage === "classification" && workflowPath === "classification" && (
          <ClassificationScreen
            onNext={() => setStage("analytics")}
            results={analysisResults.classification}
            file={analysisResults.file}
            onNewAnalysis={() => {
              setWorkflowPath(null);
              setStage("upload");
            }}
          />
        )}
        {stage === "analytics" && workflowPath === "classification" && (
          <AnalyticsDashboard
            results={analysisResults}
            workflowPath="classification"
            onNewAnalysis={() => {
              setWorkflowPath(null);
              setStage("upload");
            }}
          />
        )}

        {/* Full Analysis Path */}
        {stage === "detection" && workflowPath === "detection" && (
          <DetectionScreen
            onNext={() => setStage("segmentation")}
            results={analysisResults.detection}
            file={analysisResults.file}
          />
        )}
        {stage === "segmentation" && workflowPath === "detection" && (
          <SegmentationScreen
            onNext={() => setStage("segmentation-analytics")}
            results={analysisResults.segmentation}
            file={analysisResults.file}
          />
        )}
        {stage === "segmentation-analytics" && workflowPath === "detection" && (
          <AnalyticsDashboard
            results={analysisResults}
            workflowPath="segmentation"
            onNewAnalysis={() => {
              setWorkflowPath(null);
              setStage("upload");
            }}
          />
        )}
        {stage === "analytics" && workflowPath === "detection" && (
          <AnalyticsDashboard
            results={analysisResults}
            workflowPath="detection"
            onNewAnalysis={() => {
              setWorkflowPath(null);
              setStage("upload");
            }}
          />
        )}
      </main>

      <Footer />
    </div>
  );
}
