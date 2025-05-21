import { 
  Box, 
  SimpleGrid, 
  Stat, 
  StatLabel, 
  StatNumber, 
  StatHelpText,
  Progress,
  Text,
  Flex
} from '@chakra-ui/react';
import { EvaluationMetric } from '../../types/evaluation';

interface MetricsDashboardProps {
  metrics: EvaluationMetric[];
}

const MetricCard = ({ metric }: { metric: EvaluationMetric }) => {
  // Choose color based on metric value
  const getColorScheme = (value: number, category: string) => {
    if (category === 'latency') {
      // For latency, lower is better
      if (value < 40) return 'success';
      if (value < 70) return 'warning';
      return 'error';
    } else {
      // For other metrics, higher is better
      if (value >= 80) return 'success';
      if (value >= 60) return 'warning';
      return 'error';
    }
  };

  const colorScheme = getColorScheme(metric.value, metric.category);

  return (
    <Box p={5} borderWidth="1px" borderRadius="lg" bg="white">
      <Stat>
        <StatLabel fontSize="sm" color="gray.500" mb={1}>{metric.name}</StatLabel>
        <Flex align="center" justify="space-between">
          <StatNumber fontSize="2xl">{metric.value}%</StatNumber>
          <Box fontSize="sm" fontWeight="medium" color={`${colorScheme}.500`}>
            {colorScheme === 'success' ? 'Good' : colorScheme === 'warning' ? 'Average' : 'Poor'}
          </Box>
        </Flex>
        <Progress 
          value={metric.value} 
          colorScheme={colorScheme} 
          size="sm" 
          borderRadius="full" 
          mt={2}
        />
        <StatHelpText mt={2} fontSize="xs">{metric.description}</StatHelpText>
      </Stat>
    </Box>
  );
};

const MetricsDashboard = ({ metrics }: MetricsDashboardProps) => {
  // Group metrics by category
  const relevancyMetrics = metrics.filter(m => m.category === 'relevancy');
  const precisionMetrics = metrics.filter(m => m.category === 'precision');
  const latencyMetrics = metrics.filter(m => m.category === 'latency');

  // Calculate average scores
  const calculateAverage = (metrics: EvaluationMetric[]) => {
    if (metrics.length === 0) return 0;
    return metrics.reduce((sum, m) => sum + m.value, 0) / metrics.length;
  };

  const relevancyAvg = calculateAverage(relevancyMetrics);
  const precisionAvg = calculateAverage(precisionMetrics);
  const latencyAvg = calculateAverage(latencyMetrics);

  return (
    <Box>
      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6} mb={6}>
        <Box
          p={5}
          borderWidth="1px"
          borderRadius="lg"
          bg="white"
          boxShadow="sm"
        >
          <Text fontSize="lg" fontWeight="medium" mb={4}>
            Relevancy
          </Text>
          <Flex align="center" justify="space-between" mb={2}>
            <Text fontSize="3xl" fontWeight="bold">{relevancyAvg.toFixed(1)}%</Text>
            <Box 
              px={2} 
              py={1} 
              bg={relevancyAvg >= 80 ? 'green.100' : relevancyAvg >= 60 ? 'yellow.100' : 'red.100'}
              color={relevancyAvg >= 80 ? 'green.700' : relevancyAvg >= 60 ? 'yellow.700' : 'red.700'}
              borderRadius="md"
              fontSize="sm"
              fontWeight="medium"
            >
              {relevancyAvg >= 80 ? 'Good' : relevancyAvg >= 60 ? 'Average' : 'Poor'}
            </Box>
          </Flex>
          <Progress 
            value={relevancyAvg} 
            colorScheme={relevancyAvg >= 80 ? 'green' : relevancyAvg >= 60 ? 'yellow' : 'red'} 
            size="sm" 
            borderRadius="full"
          />
        </Box>

        <Box
          p={5}
          borderWidth="1px"
          borderRadius="lg"
          bg="white"
          boxShadow="sm"
        >
          <Text fontSize="lg" fontWeight="medium" mb={4}>
            Context Precision
          </Text>
          <Flex align="center" justify="space-between" mb={2}>
            <Text fontSize="3xl" fontWeight="bold">{precisionAvg.toFixed(1)}%</Text>
            <Box 
              px={2} 
              py={1} 
              bg={precisionAvg >= 80 ? 'green.100' : precisionAvg >= 60 ? 'yellow.100' : 'red.100'}
              color={precisionAvg >= 80 ? 'green.700' : precisionAvg >= 60 ? 'yellow.700' : 'red.700'}
              borderRadius="md"
              fontSize="sm"
              fontWeight="medium"
            >
              {precisionAvg >= 80 ? 'Good' : precisionAvg >= 60 ? 'Average' : 'Poor'}
            </Box>
          </Flex>
          <Progress 
            value={precisionAvg} 
            colorScheme={precisionAvg >= 80 ? 'green' : precisionAvg >= 60 ? 'yellow' : 'red'} 
            size="sm" 
            borderRadius="full"
          />
        </Box>

        <Box
          p={5}
          borderWidth="1px"
          borderRadius="lg"
          bg="white"
          boxShadow="sm"
        >
          <Text fontSize="lg" fontWeight="medium" mb={4}>
            Response Latency
          </Text>
          <Flex align="center" justify="space-between" mb={2}>
            <Text fontSize="3xl" fontWeight="bold">{latencyAvg.toFixed(1)}%</Text>
            <Box 
              px={2} 
              py={1} 
              bg={latencyAvg < 40 ? 'green.100' : latencyAvg < 70 ? 'yellow.100' : 'red.100'}
              color={latencyAvg < 40 ? 'green.700' : latencyAvg < 70 ? 'yellow.700' : 'red.700'}
              borderRadius="md"
              fontSize="sm"
              fontWeight="medium"
            >
              {latencyAvg < 40 ? 'Fast' : latencyAvg < 70 ? 'Medium' : 'Slow'}
            </Box>
          </Flex>
          <Progress 
            value={latencyAvg} 
            colorScheme={latencyAvg < 40 ? 'green' : latencyAvg < 70 ? 'yellow' : 'red'} 
            size="sm" 
            borderRadius="full"
          />
        </Box>
      </SimpleGrid>

      <Text fontSize="xl" fontWeight="semibold" mb={4}>
        Detailed Metrics
      </Text>
      <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
        {metrics.map((metric) => (
          <MetricCard key={metric.id} metric={metric} />
        ))}
      </SimpleGrid>
    </Box>
  );
};

export default MetricsDashboard;