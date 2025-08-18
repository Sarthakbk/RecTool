import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { PlusIcon, PencilIcon, TrashIcon, EyeIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import jdService from '../services/jdService';
import SectionHeader from '../components/SectionHeader';

const JDReport = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedJob, setSelectedJob] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const location = useLocation();
  const highlightId = location.state?.highlightId;

  useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = async () => {
    try {
      setLoading(true);
      const response = await jdService.getAllJobs();
      setJobs(response.data || []);
    } catch (error) {
      toast.error('Failed to load job descriptions');
      console.error('Error loading jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (jobId) => {
    if (window.confirm('Are you sure you want to delete this job description?')) {
      try {
        await jdService.deleteJob(jobId);
        toast.success('Job description deleted successfully');
        loadJobs();
      } catch (error) {
        toast.error('Failed to delete job description');
      }
    }
  };

  const handleView = (job) => {
    setSelectedJob(job);
    setShowModal(true);
  };

  const formatSkills = (skills) => {
    if (!skills) return 'N/A';
    try {
      const skillsArray = typeof skills === 'string' ? JSON.parse(skills) : skills;
      return Array.isArray(skillsArray) ? skillsArray.join(', ') : 'N/A';
    } catch {
      return skills || 'N/A';
    }
  };

  const formatKeywords = (keywords) => {
    if (!keywords) return 'N/A';
    try {
      const keywordsArray = typeof keywords === 'string' ? JSON.parse(keywords) : keywords;
      return Array.isArray(keywordsArray) ? keywordsArray.join(', ') : 'N/A';
    } catch {
      return keywords || 'N/A';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Open': return 'bg-green-100 text-green-800';
      case 'In Progress': return 'bg-blue-100 text-blue-800';
      case 'On Hold': return 'bg-yellow-100 text-yellow-800';
      case 'Closed': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getModeColor = (mode) => {
    switch (mode) {
      case 'Remote': return 'bg-purple-100 text-purple-800';
      case 'Onsite': return 'bg-indigo-100 text-indigo-800';
      case 'Hybrid': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading job descriptions...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <SectionHeader 
          title="Job Description Report"
          subtitle={`Showing ${jobs.length} job descriptions`}
        />

        {/* Action Bar */}
        <div className="mb-6 flex justify-end">
          <Link
            to="/"
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Add New Job
          </Link>
        </div>

        {/* Jobs Table */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Company</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Mode</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tenure</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Experience</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Budget</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Positions</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Aging</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created By</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className= "bg-white divide-y divide-gray-200">
                {jobs.map((job) => (
                  <tr key={job.jd_id} className="hover:bg-gray-50">
                    <td className={`px-6 py-4 text-sm ${highlightId && Number(highlightId) === Number(job.jd_id) ? 'bg-yellow-50 font-semibold text-gray-900' : 'text-gray-900'}`}>{job.customer_name || 'Sample Company'}</td>
                    <td className="px-6 py-4 text-sm text-gray-900">{job.jd_consumer || '—'}</td>
                    <td className="px-6 py-4 text-sm text-gray-900">{job.job_mode_name}</td>
                    <td className="px-6 py-4 text-sm text-gray-900">{job.jd_tenure} mo</td>
                    <td className="px-6 py-4 text-sm text-gray-900">{job.jd_op_exp_min}-{job.jd_op_exp_max} yrs</td>
                    <td className="px-6 py-4 text-sm text-gray-900">{(job.jd_currency === 'INR' ? '₹' : '$')}{job.jd_op_budget_min?.toLocaleString()}-{(job.jd_currency === 'INR' ? '₹' : '$')}{job.jd_op_budget_max?.toLocaleString()}</td>
                    <td className="px-6 py-4 text-sm text-gray-900">{job.jd_open_position || 'N/A'}</td>
                    <td className="px-6 py-4 text-sm">
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(job.job_status_name)}`}>{job.job_status_name}</span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">{job.jd_aging || 0} days</td>
                    <td className="px-6 py-4 text-sm text-gray-900">{job.created_by_name}</td>

                    {/* Actions Column */}
                    <td className="px-6 py-4">
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleView(job)}
                          className="text-blue-600 hover:text-blue-900"
                          title="View Details"
                        >
                          <EyeIcon className="h-5 w-5" />
                        </button>
                        <Link
                          to={`/edit/${job.jd_id}`}
                          className="text-green-600 hover:text-green-900"
                          title="Edit"
                        >
                          <PencilIcon className="h-5 w-5" />
                        </Link>
                        <button
                          onClick={() => handleDelete(job.jd_id)}
                          className="text-red-600 hover:text-red-900"
                          title="Delete"
                        >
                          <TrashIcon className="h-5 w-5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {jobs.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-500">No job descriptions found.</p>
              <Link
                to="/"
                className="mt-4 inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                <PlusIcon className="h-5 w-5 mr-2" />
                Create Your First Job Description
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Job Details Modal */}
      {showModal && selectedJob && (
        <div className="fixed inset-0 z-50">
          <div className="absolute inset-0 bg-gray-900/60" onClick={() => setShowModal(false)} />
          <div className="relative mx-auto top-16 w-11/12 md:w-4/5 lg:w-3/4 max-w-5xl bg-white rounded-xl shadow-2xl border">
            {/* Header */}
            <div className="sticky top-0 flex items-center justify-between px-6 py-4 border-b bg-white/90 backdrop-blur">
              <div>
                <h3 className="text-xl font-semibold text-gray-900">{selectedJob.jd_title}</h3>
                <p className="text-xs text-gray-500">ID: {selectedJob.jd_id}</p>
              </div>
              <button
                onClick={() => setShowModal(false)}
                className="inline-flex items-center justify-center h-9 w-9 rounded-full text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition"
                aria-label="Close"
              >
                <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Body */}
            <div className="p-6 max-h-[70vh] overflow-y-auto space-y-6">
              {/* Top badges */}
              <div className="flex flex-wrap items-center gap-3">
                <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${getStatusColor(selectedJob.job_status_name)}`}>
                  {selectedJob.job_status_name}
                </span>
                <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${getModeColor(selectedJob.job_mode_name)}`}>
                  {selectedJob.job_mode_name}
                </span>
                <span className="text-xs text-gray-500">Created: {new Date(selectedJob.jd_created_date).toLocaleDateString()}</span>
                <span className="text-xs text-gray-500">Aging: {selectedJob.jd_aging || 0} days</span>
              </div>

              {/* Overview */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="rounded-lg border bg-gray-50 p-4">
                  <p className="text-xs text-gray-500">Customer</p>
                  <p className="text-sm font-medium text-gray-900">{selectedJob.customer_name || '—'}</p>
                </div>
                <div className="rounded-lg border bg-gray-50 p-4">
                  <p className="text-xs text-gray-500">Company</p>
                  <p className="text-sm font-medium text-gray-900">{selectedJob.jd_consumer || '—'}</p>
                </div>
                <div className="rounded-lg border bg-gray-50 p-4">
                  <p className="text-xs text-gray-500">Experience</p>
                  <p className="text-sm font-medium text-gray-900">{selectedJob.jd_op_exp_min}-{selectedJob.jd_op_exp_max} yrs</p>
                </div>
                <div className="rounded-lg border bg-gray-50 p-4">
                  <p className="text-xs text-gray-500">Budget</p>
                  <p className="text-sm font-medium text-gray-900">
                    {selectedJob.jd_currency === 'INR' ? '₹' : '$'}{selectedJob.jd_op_budget_min?.toLocaleString()} - {selectedJob.jd_currency === 'INR' ? '₹' : '$'}{selectedJob.jd_op_budget_max?.toLocaleString()}
                  </p>
                </div>
              </div>

              {/* Description */}
              <div>
                <h4 className="text-sm font-semibold text-gray-900 mb-2">Description</h4>
                <div className="rounded-lg border p-4 bg-white max-h-60 overflow-y-auto">
                  <p className="whitespace-pre-line text-sm text-gray-800">{selectedJob.jd_original}</p>
                </div>
              </div>

              {/* Details grid */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="space-y-3">
                  <h4 className="text-sm font-semibold text-gray-900">Role Details</h4>
                  <div className="rounded-lg border divide-y">
                    <div className="flex items-center justify-between p-3 text-sm">
                      <span className="text-gray-500">Tenure</span>
                      <span className="font-medium text-gray-900">{selectedJob.jd_tenure} months</span>
                    </div>
                    <div className="flex items-center justify-between p-3 text-sm">
                      <span className="text-gray-500">Positions</span>
                      <span className="font-medium text-gray-900">{selectedJob.jd_open_position || '—'}</span>
                    </div>
                    <div className="flex items-center justify-between p-3 text-sm">
                      <span className="text-gray-500">Revenue Potential</span>
                      <span className="font-medium text-gray-900">{selectedJob.jd_revenue_potential || '—'}</span>
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  <h4 className="text-sm font-semibold text-gray-900">Ownership</h4>
                  <div className="rounded-lg border divide-y">
                    <div className="flex items-center justify-between p-3 text-sm">
                      <span className="text-gray-500">Created By</span>
                      <span className="font-medium text-gray-900">{selectedJob.created_by_name || selectedJob.jd_created_by || '—'}</span>
                    </div>
                    <div className="flex items-center justify-between p-3 text-sm">
                      <span className="text-gray-500">Source</span>
                      <span className="font-medium text-gray-900">{selectedJob.jd_source || '—'}</span>
                    </div>
                    <div className="p-3 text-sm">
                      <span className="block text-gray-500 mb-1">Special Instruction</span>
                      <span className="block font-medium text-gray-900 whitespace-pre-line">{selectedJob.jd_special_instruction || '—'}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Skills & Keywords */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <h4 className="text-sm font-semibold text-gray-900 mb-2">Skills</h4>
                  <div className="rounded-lg border p-3 bg-white min-h-[52px]">
                    <div className="flex flex-wrap gap-2">
                      {(Array.isArray(selectedJob.jd_skillset) ? selectedJob.jd_skillset : (selectedJob.jd_skillset ? [selectedJob.jd_skillset] : []))
                        .map((s, idx) => (
                          <span key={idx} className="inline-flex items-center px-2.5 py-1 rounded-full text-xs bg-blue-50 text-blue-700 border border-blue-200">{s}</span>
                        ))}
                      {(!selectedJob.jd_skillset || (Array.isArray(selectedJob.jd_skillset) && selectedJob.jd_skillset.length === 0)) && (
                        <span className="text-xs text-gray-500">—</span>
                      )}
                    </div>
                  </div>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-gray-900 mb-2">Keywords</h4>
                  <div className="rounded-lg border p-3 bg-white min-h-[52px]">
                    <div className="flex flex-wrap gap-2">
                      {(Array.isArray(selectedJob.jd_keywords) ? selectedJob.jd_keywords : (selectedJob.jd_keywords ? [selectedJob.jd_keywords] : []))
                        .map((k, idx) => (
                          <span key={idx} className="inline-flex items-center px-2.5 py-1 rounded-full text-xs bg-emerald-50 text-emerald-700 border border-emerald-200">{k}</span>
                        ))}
                      {(!selectedJob.jd_keywords || (Array.isArray(selectedJob.jd_keywords) && selectedJob.jd_keywords.length === 0)) && (
                        <span className="text-xs text-gray-500">—</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Footer */}
            <div className="px-6 py-4 border-t bg-gray-50 rounded-b-xl flex justify-end">
              <button
                onClick={() => setShowModal(false)}
                className="inline-flex items-center px-4 py-2 rounded-md bg-gray-800 text-white hover:bg-gray-900 transition"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default JDReport; 