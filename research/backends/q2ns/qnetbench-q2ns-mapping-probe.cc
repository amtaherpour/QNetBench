/* QNetBench Checkpoint 9 research probe for Q2NS.
 * Research evidence only; this is not a production adapter.
 */

#include "ns3/core-module.h"
#include "ns3/internet-module.h"
#include "ns3/network-module.h"
#include "ns3/q2ns-analysis.h"
#include "ns3/q2ns-classical-network-builder.h"
#include "ns3/q2ns-netcontroller.h"
#include "ns3/q2ns-qnode.h"
#include "ns3/q2ns-swap-app.h"
#include "ns3/q2ns-swap-helper.h"
#include "ns3/q2ns-qubit.h"
#include "ns3/simulator.h"

#include <algorithm>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using namespace ns3;
using namespace q2ns;

namespace {

constexpr uint32_t kRequestCount = 16;
constexpr double kDeadlineSeconds = 1.0;
constexpr double kFrequencyHz = 1000.0;
constexpr double kQuantumDelayNsPerKm = 5000.0;

struct NativeRecord {
  uint64_t sid;
  double terminalSeconds;
  double fidelity;
};

std::vector<NativeRecord> g_chainRecords;

void OnVerifyFidelity(uint64_t sid, Time terminal, double fidelity) {
  g_chainRecords.push_back({sid, terminal.GetSeconds(), fidelity});
}

std::string Escape(const std::string& value) {
  std::ostringstream out;
  for (char ch : value) {
    switch (ch) {
    case '\\':
      out << "\\\\";
      break;
    case '"':
      out << "\\\"";
      break;
    case '\n':
      out << "\\n";
      break;
    case '\r':
      out << "\\r";
      break;
    case '\t':
      out << "\\t";
      break;
    default:
      out << ch;
    }
  }
  return out.str();
}

std::string RecordJson(uint64_t sid, const std::string& source,
                       const std::string& destination,
                       const std::vector<std::string>& path,
                       const NativeRecord* native) {
  std::ostringstream out;
  out << std::setprecision(17);
  out << "{\"request_id\":\"request-" << std::setw(4) << std::setfill('0')
      << sid << std::setfill(' ') << "\",\"source\":\"" << source
      << "\",\"destination\":\"" << destination << "\",";
  if (native) {
    out << "\"submitted_at_s\":0,\"terminal_at_s\":"
        << native->terminalSeconds
        << ",\"status\":\"success\",\"latency_s\":"
        << native->terminalSeconds << ",\"fidelity\":" << native->fidelity
        << ",\"attempts\":null,";
  } else {
    out << "\"submitted_at_s\":0,\"terminal_at_s\":1,"
        << "\"status\":\"timed_out\",\"latency_s\":1,"
        << "\"fidelity\":null,\"attempts\":null,";
  }
  out << "\"path\":[";
  for (size_t index = 0; index < path.size(); ++index) {
    if (index)
      out << ',';
    out << '"' << Escape(path[index]) << '"';
  }
  out << "],\"failure_reason\":";
  if (native)
    out << "null";
  else
    out << "\"Q2NS micro-scenario exceeded the benchmark deadline\"";
  out << ",\"metadata\":{\"simulator\":\"q2ns\","
      << "\"classification\":\""
      << (native ? "native_event_derived_request_record" : "derived_timeout")
      << "\"";
  if (native)
    out << ",\"native_terminal_ns\":"
        << native->terminalSeconds * 1e9;
  out << "}}";
  return out.str();
}

std::string ScenarioJson(const std::string& scenario, uint64_t seed,
                         bool controlledFailure,
                         const std::vector<std::string>& path,
                         std::vector<NativeRecord> nativeRecords) {
  std::sort(nativeRecords.begin(), nativeRecords.end(),
            [](const NativeRecord& left, const NativeRecord& right) {
              return left.sid < right.sid;
            });
  std::map<uint64_t, NativeRecord> bySid;
  for (const auto& record : nativeRecords)
    bySid.emplace(record.sid, record);

  std::ostringstream out;
  out << "{\"scenario\":\"" << scenario << "\",\"seed\":" << seed
      << ",\"controlled_failure\":"
      << (controlledFailure ? "true" : "false")
      << ",\"native_time_unit\":\"nanosecond\","
      << "\"records\":[";
  for (uint64_t sid = 1; sid <= kRequestCount; ++sid) {
    if (sid > 1)
      out << ',';
    auto iterator = bySid.find(sid);
    const NativeRecord* record =
        iterator == bySid.end() ? nullptr : &iterator->second;
    out << RecordJson(sid, "node-0", path.back(), path, record);
  }
  out << "]}";
  return out.str();
}

std::string RunDirect(uint64_t seed, bool controlledFailure) {
  RngSeedManager::SetSeed(seed);
  RngSeedManager::SetRun(1);
  NetController net;
  auto referenceNode = net.CreateNode();
  auto referencePair = referenceNode->CreateBellPair();
  const auto ideal = net.GetState(referencePair.first);
  auto source = net.CreateNode();
  auto destination = net.CreateNode();
  auto channel = net.InstallQuantumLink(source, destination);
  const double delayNs = controlledFailure ? 2e9 : 20.0 * kQuantumDelayNsPerKm;
  channel->SetAttribute(
      "Delay",
      TimeValue(NanoSeconds(static_cast<uint64_t>(delayNs))));

  std::vector<std::shared_ptr<Qubit>> held;
  std::vector<NativeRecord> records;
  destination->SetRecvCallback(
      [&net, &ideal, &records](std::shared_ptr<Qubit> qubit) {
        if (!qubit)
          return;
        const std::string& label = qubit->GetLabel();
        const std::string prefix = "qnb_link_";
        if (label.rfind(prefix, 0) != 0)
          return;
        const auto sid = std::stoull(label.substr(prefix.size()));
        auto actual = net.GetState(qubit);
        if (!actual || !ideal)
          throw std::runtime_error("Q2NS direct scenario lacks a quantum state");
        const double fidelity = q2ns::analysis::Fidelity(*actual, *ideal);
        records.push_back({sid, Simulator::Now().GetSeconds(), fidelity});
      });

  for (uint64_t sid = 1; sid <= kRequestCount; ++sid) {
    const double start = static_cast<double>(sid - 1) / kFrequencyHz;
    Simulator::Schedule(Seconds(start), [source, destination, sid, &held]() {
      auto pair = source->CreateBellPair();
      held.push_back(pair.first);
      pair.second->SetLabel("qnb_link_" + std::to_string(sid));
      if (!source->Send(pair.second, destination->GetId()))
        throw std::runtime_error("Q2NS direct quantum send failed");
    });
  }
  Simulator::Stop(Seconds(kDeadlineSeconds));
  Simulator::Run();
  Simulator::Destroy();
  return ScenarioJson(
      "qnb-v0-1-link-2-batch", seed, controlledFailure,
      {"node-0", "node-1"}, records);
}

ClassicalNetworkBuilder::Link ClassicalLink(const std::string& id,
                                             const std::string& left,
                                             const std::string& right) {
  ClassicalNetworkBuilder::Link link;
  link.id = id;
  link.nodeA = left;
  link.nodeB = right;
  link.rate = "10Gbps";
  link.delay = "50us";
  return link;
}

std::string RunChain(uint64_t seed, bool controlledFailure) {
  RngSeedManager::SetSeed(seed);
  RngSeedManager::SetRun(1);
  g_chainRecords.clear();

  NetController net;
  auto node0 = net.CreateNode();
  auto node1 = net.CreateNode();
  auto node2 = net.CreateNode();
  std::map<std::string, Ptr<QNode>> nodes = {
      {"node-0", node0}, {"node-1", node1}, {"node-2", node2}};

  auto classical = CreateObject<ClassicalNetworkBuilder>();
  classical->SetIpVersion(ClassicalNetworkBuilder::IpVersion::V4);
  classical->SetRouting(ClassicalNetworkBuilder::Routing::Global);
  for (const auto& [name, node] : nodes)
    classical->AttachNode(name, node);
  classical->AddLink(ClassicalLink("c01", "node-0", "node-1"));
  classical->AddLink(ClassicalLink("c12", "node-1", "node-2"));
  auto handle = classical->Build();

  SwapTopologySpec topology;
  topology.nodes = {"node-0", "node-1", "node-2"};
  const double delayPerKm =
      controlledFailure ? 200'000'000.0 : kQuantumDelayNsPerKm;
  topology.quantumEdges = {
      {"node-0", "node-1", 10.0, delayPerKm},
      {"node-1", "node-2", 10.0, delayPerKm},
  };
  topology.classicalEdges = {
      {"node-0", "node-1", 10'000.0, "udp", 5000.0, 10.0,
       "128kB"},
      {"node-1", "node-2", 10'000.0, "udp", 5000.0, 10.0,
       "128kB"},
  };
  for (uint64_t sid = 1; sid <= kRequestCount; ++sid) {
    topology.sessions.push_back(
        {{"node-0", "node-1", "node-2"},
         static_cast<double>(sid - 1) / kFrequencyHz, sid, 0, "udp"});
  }

  EntanglementSwapHelper helper;
  helper.SetNetController(&net).SetNodes(nodes).Install(topology, handle, false);
  const std::string tracePath =
      "/NodeList/*/ApplicationList/*/$q2ns::SwapApp/VerifyFidelity";
  Config::ConnectWithoutContext(tracePath, MakeCallback(&OnVerifyFidelity));
  Simulator::Stop(Seconds(kDeadlineSeconds));
  Simulator::Run();
  Config::DisconnectWithoutContext(tracePath, MakeCallback(&OnVerifyFidelity));
  Simulator::Destroy();
  return ScenarioJson(
      "qnb-v0-1-chain-3-batch", seed, controlledFailure,
      {"node-0", "node-1", "node-2"}, g_chainRecords);
}

size_t CountSuccesses(const std::string& scenarioJson) {
  const std::string marker = "\"status\":\"success\"";
  size_t count = 0;
  size_t position = 0;
  while ((position = scenarioJson.find(marker, position)) != std::string::npos) {
    ++count;
    position += marker.size();
  }
  return count;
}

std::string EvidenceJson() {
  const auto link = RunDirect(7, false);
  const auto linkRepeat = RunDirect(7, false);
  const auto linkAlternate = RunDirect(8, false);
  const auto linkFailure = RunDirect(7, true);
  const auto chain = RunChain(7, false);
  const auto chainRepeat = RunChain(7, false);
  const auto chainAlternate = RunChain(8, false);
  const auto chainFailure = RunChain(7, true);

  if (link != linkRepeat)
    throw std::runtime_error("Q2NS link same-seed repeat is not identical");
  if (chain != chainRepeat)
    throw std::runtime_error("Q2NS chain same-seed repeat is not identical");
  if (CountSuccesses(link) == 0 || CountSuccesses(chain) == 0)
    throw std::runtime_error("Q2NS normal micro-scenario produced no success");
  if (CountSuccesses(linkFailure) != 0 || CountSuccesses(chainFailure) != 0)
    throw std::runtime_error("Q2NS controlled-failure scenario produced a success");

  std::ostringstream out;
  out << "{\"evidence_schema_version\":\"1.0\","
      << "\"simulator_id\":\"q2ns\","
      << "\"q2ns_commit\":\"f22ba28f437099ba3cf9956ca332ba5ce8bb14fd\","
      << "\"ns3_commit\":\"e2c9e30c6ebdfd534aa7e30f6324b5674d138b9f\","
      << "\"same_seed_identical\":true,\"cases\":{"
      << "\"qnb-v0-1-link-2-batch\":{\"normal\":" << link
      << ",\"alternate_seed\":" << linkAlternate
      << ",\"controlled_failure\":" << linkFailure << "},"
      << "\"qnb-v0-1-chain-3-batch\":{\"normal\":" << chain
      << ",\"alternate_seed\":" << chainAlternate
      << ",\"controlled_failure\":" << chainFailure << "}}}";
  return out.str();
}

} // namespace

int main(int argc, char* argv[]) {
  std::string output;
  CommandLine command;
  command.AddValue("output", "Output JSON path", output);
  command.Parse(argc, argv);
  if (output.empty())
    throw std::runtime_error("--output is required");
  const std::string evidence = EvidenceJson();
  std::ofstream stream(output);
  if (!stream)
    throw std::runtime_error("could not open output path");
  stream << evidence << '\n';
  std::cout << "QNetBench Q2NS mapping probe passed\n";
  return 0;
}
