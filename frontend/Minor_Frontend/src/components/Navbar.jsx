import React from "react";
import { Activity, Menu, Settings, Home, BarChart3 } from "lucide-react";

export default function Navbar({ setStage, workflowPath }) {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  // Navigation items based on workflow
  const navItems = workflowPath
    ? [
        { label: "UPLOAD", stage: "upload", icon: Home },
        workflowPath === "classification"
          ? { label: "CLASSIFICATION", stage: "classification", icon: Activity }
          : { label: "RESULTS", stage: "analytics", icon: BarChart3 },
      ]
    : [
        { label: "UPLOAD", stage: "upload", icon: Home },
        { label: "RESULTS", stage: "analytics", icon: BarChart3 },
      ];

  return (
    <nav className="bg-gradient-to-r from-cyan-600 via-blue-600 to-blue-700 shadow-lg sticky top-0 z-40">
      <div className="max-w-full px-2 py-0 h-20 flex items-center">
        <div className="flex items-center justify-between w-full">
          {/* Logo Section */}
          <div
            className="flex items-center gap-2 cursor-pointer group hover:scale-105 transition-transform"
            onClick={() => setStage("upload")}
          >
            <div className="bg-white p-1 rounded-md shadow-sm group-hover:shadow-md transition-shadow">
              <Activity className="text-cyan-600" size={18} />
            </div>
            <div className="flex flex-col leading-tight">
              <h1 className="font-bold text-xs text-white tracking-tight leading-none">
                NeuroPath AI
              </h1>
              <p className="text-cyan-100 text-[10px] font-medium leading-none -mt-0.5">
                Medical Imaging
              </p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-4">
            {navItems.map(({ label, stage, icon: Icon }) => (
              <button
                key={stage}
                onClick={() => setStage(stage)}
                className="flex items-center gap-1 px-2.5 py-1 bg-white/10 hover:bg-white/20 text-white rounded-md font-medium transition-all hover:scale-105 active:scale-95 backdrop-blur-sm text-xs"
              >
                <Icon size={14} />
                {label}
              </button>
            ))}
            {workflowPath && (
              <div className="flex items-center gap-1 px-2 py-1 bg-blue-400/20 text-blue-100 rounded-md font-semibold text-[10px]">
                <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse" />
                {workflowPath === "classification"
                  ? "Classification"
                  : "Full Analysis"}
              </div>
            )}
            <div className="flex items-center gap-1 px-2 py-1 bg-green-400/20 text-green-100 rounded-md font-semibold text-[10px]">
              <div className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse" />
              v2.4
            </div>
            <button className="p-1 hover:bg-white/10 rounded-md transition-colors">
              <Settings className="text-white" size={14} />
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 hover:bg-white/10 rounded-lg transition-colors"
          >
            <Menu className="text-white" size={20} />
          </button>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden mt-2 flex flex-col gap-2 border-t border-white/20 pt-2">
            {navItems.map(({ label, stage, icon: Icon }) => (
              <button
                key={stage}
                onClick={() => {
                  setStage(stage);
                  setMobileMenuOpen(false);
                }}
                className="flex items-center gap-2 px-3 py-1.5 bg-white/10 hover:bg-white/20 text-white rounded-lg font-semibold transition-all w-full text-sm"
              >
                <Icon size={16} />
                {label}
              </button>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
}
