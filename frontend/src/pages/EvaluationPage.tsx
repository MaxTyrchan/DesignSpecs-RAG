import { useState } from "react";
import {
  Container,
  Box,
  Heading,
  Text,
  useToast,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  Flex,
  Button,
} from "@chakra-ui/react";
import { Play, } from "lucide-react";
import MetricsDashboard from "../components/Evaluation/MetricsDashboard";
import QueryResponsePairComponent from "../components/Evaluation/QueryResponsePair";
import EvaluationFilters from "../components/Evaluation/EvaluationFilters";
import {
  EvaluationMetric,
  QueryResponsePair,
  EvaluationType,
} from "../types/evaluation";
import API from "../api/api";

const api = API.getInstance();

// Mock data
const mockMetrics: EvaluationMetric[] = [
  {
    id: "1",
    name: "Overall Accuracy",
    value: 87,
    description: "How accurate the responses are across all queries",
    category: "relevancy",
  },
  {
    id: "2",
    name: "Context Usage",
    value: 92,
    description: "How effectively the model uses the provided context",
    category: "precision",
  },
  {
    id: "3",
    name: "Answer Completeness",
    value: 78,
    description: "How complete the answers are",
    category: "relevancy",
  },
  {
    id: "4",
    name: "Response Time",
    value: 35,
    description: "Average time to generate responses",
    category: "latency",
  },
  {
    id: "5",
    name: "Factual Correctness",
    value: 84,
    description: "Accuracy of facts in responses",
    category: "precision",
  },
  {
    id: "6",
    name: "Citation Accuracy",
    value: 76,
    description: "Accuracy of citations and references",
    category: "precision",
  },
  {
    id: "7",
    name: "Consistency",
    value: 83,
    description: "Consistency of responses across similar queries",
    category: "relevancy",
  },
  {
    id: "8",
    name: "Processing Overhead",
    value: 42,
    description: "Computational resources used",
    category: "latency",
  },
  {
    id: "9",
    name: "Query Understanding",
    value: 89,
    description: "How well the system understands user questions",
    category: "relevancy",
  },
];

const mockPairs: QueryResponsePair[] = [
  {
    id: "1",
    query: "What are the key factors affecting global climate change?",
    response:
      "Based on the documents you provided, the key factors affecting global climate change include greenhouse gas emissions (primarily CO2, methane, and nitrous oxide), deforestation, industrial processes, and agricultural practices.",
    timestamp: new Date("2023-06-15T14:32:21"),
    metrics: [
      {
        id: "101",
        name: "Relevancy",
        value: 92,
        description: "How relevant the response is to the query",
        category: "relevancy",
      },
      {
        id: "102",
        name: "Context Usage",
        value: 88,
        description: "How well the context was utilized",
        category: "precision",
      },
      {
        id: "103",
        name: "Latency",
        value: 28,
        description: "Response time in milliseconds",
        category: "latency",
      },
    ],
    groundTruth:
      "The key factors affecting global climate change are anthropogenic greenhouse gas emissions (CO2, methane, nitrous oxide), deforestation, industrial processes, agricultural practices, and changes in land use patterns.",
  },
  {
    id: "2",
    query: "Summarize the main points of the financial report.",
    response:
      "The financial report highlights strong revenue growth of 18% year-over-year, reaching $2.3B. Operating margin improved to 24% from 21% last year. However, there were challenges in the European market with a 5% decline in sales. The report recommends expanding into Asian markets and cutting operational costs by 8%.",
    timestamp: new Date("2023-06-14T09:15:43"),
    metrics: [
      {
        id: "201",
        name: "Relevancy",
        value: 85,
        description: "How relevant the response is to the query",
        category: "relevancy",
      },
      {
        id: "202",
        name: "Context Usage",
        value: 90,
        description: "How well the context was utilized",
        category: "precision",
      },
      {
        id: "203",
        name: "Latency",
        value: 42,
        description: "Response time in milliseconds",
        category: "latency",
      },
    ],
  },
  {
    id: "3",
    query:
      "What are the side effects of medication X according to the clinical trials?",
    response:
      "According to the clinical trials documented in the provided papers, medication X showed side effects including headache (reported by 15% of participants), nausea (12%), insomnia (8%), and mild dizziness (7%). Severe side effects were rare, with allergic reactions occurring in less than 1% of participants.",
    timestamp: new Date("2023-06-13T16:47:32"),
    metrics: [
      {
        id: "301",
        name: "Relevancy",
        value: 94,
        description: "How relevant the response is to the query",
        category: "relevancy",
      },
      {
        id: "302",
        name: "Context Usage",
        value: 92,
        description: "How well the context was utilized",
        category: "precision",
      },
      {
        id: "303",
        name: "Latency",
        value: 31,
        description: "Response time in milliseconds",
        category: "latency",
      },
    ],
    groundTruth:
      "The clinical trials for medication X documented the following side effects: headache (15.2% of participants), nausea (11.8%), insomnia (7.9%), dizziness (6.7%), and allergic reactions (0.8%).",
  },
];

const EvaluationPage = () => {
  const [metrics, setMetrics] = useState<EvaluationMetric[]>(mockMetrics);
  const [queryPairs, setQueryPairs] = useState<QueryResponsePair[]>(mockPairs);
  const [isLoading, setIsLoading] = useState(false);
  const [evaluationType, setEvaluationType] =
    useState<EvaluationType>("openevals");
  const [maxExamples, setMaxExamples] = useState<number>(7); // Default to all examples
  const [evaluationSummary, setEvaluationSummary] = useState<any>(null);
  const toast = useToast();

  const handleExport = () => {
    toast({
      title: "Export Started",
      description: "Your evaluation data is being exported",
      status: "success",
      duration: 3000,
      isClosable: true,
    });
  };

  const handleTriggerEvaluation = async () => {
    setIsLoading(true);
    try {
      // Use the existing separate endpoints based on evaluation type
      const result = await api.getEvaluationByType(evaluationType);

      setMetrics(result.metrics);
      setQueryPairs(result.pairs || []);
      setEvaluationSummary(result.evaluation_summary);

      // Show success message with evaluation details
      const evaluationTypeLabel = {
        openevals: "OpenEvals",
        ragas: "Ragas",
        hybrid: "Hybrid (OpenEvals + Ragas)",
      }[evaluationType];

      toast({
        title: "Evaluation Complete",
        description: `${evaluationTypeLabel} evaluation completed successfully with ${result.metrics.length} metrics`,
        status: "success",
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: "Evaluation Failed",
        description:
          error instanceof Error
            ? error.message
            : "Failed to complete the evaluation. Please try again.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxW="container.xl" py={8}>
      <Box mb={8}>
        <Flex justify="space-between" align="center">
          <Box>
            <Heading as="h1" size="xl" mb={2}>
              Model Evaluation
            </Heading>
            <Text color="gray.600">
              Analyze the performance and accuracy of your RAG implementation
            </Text>
          </Box>
          <Button
            leftIcon={<Play size={16} />}
            colorScheme="green"
            onClick={handleTriggerEvaluation}
            isLoading={isLoading}
            loadingText="Evaluating..."
          >
            Run Evaluation
          </Button>
        </Flex>
      </Box>

      <Tabs colorScheme="brand" isLazy>
        <TabList mb={4}>
          <Tab fontWeight="medium">Performance Dashboard</Tab>
        </TabList>

        <TabPanels>
          <TabPanel px={0}>
            <MetricsDashboard metrics={metrics} />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Container>
  );
};

export default EvaluationPage;
