interface Step {
  agent: string;
  status: string;
  message: string;
}

export default function ExecutionTimeline({
  steps,
}: {
  steps: Step[];
}) {
  return (
    <div className="rounded-xl border p-4 mt-4 bg-white">
      <h2 className="font-bold text-lg mb-4">
        ⚡ AI Execution
      </h2>

      {steps.map((step, i) => (
        <div
          key={i}
          className="flex items-start gap-3 mb-3"
        >
          <div className="w-3 h-3 rounded-full bg-green-500 mt-2" />

          <div>
            <div className="font-semibold">
              {step.agent}
            </div>

            <div className="text-gray-500 text-sm">
              {step.message}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}