import { 
  Box, 
  HStack, 
  Select, 
  RangeSlider,
  RangeSliderTrack,
  RangeSliderFilledTrack,
  RangeSliderThumb,
  Text,
  Button,
  Flex,
  Badge,
  Divider
} from '@chakra-ui/react';

interface EvaluationFiltersProps {
  onExport: () => void;
}

const EvaluationFilters = ({ onExport }: EvaluationFiltersProps) => {
  return (
    <Box 
      p={5} 
      bg="white" 
      borderRadius="lg"
      borderWidth="1px"
      mb={6}
    >
      <Flex 
        justify="space-between" 
        align={{ base: "stretch", md: "center" }}
        direction={{ base: "column", md: "row" }}
        mb={4}
        gap={4}
      >
        <Text fontSize="lg" fontWeight="medium">
          Evaluation Filters
        </Text>
        
        <Button 
          colorScheme="brand" 
          size="sm"
          onClick={onExport}
        >
          Export Results
        </Button>
      </Flex>
      
      <Divider mb={4} />
      
      <Flex 
        gap={6} 
        direction={{ base: "column", md: "row" }}
        wrap="wrap"
      >
        <Box flex="1" minW={{ base: "100%", md: "200px" }}>
          <Text fontSize="sm" fontWeight="medium" mb={2}>
            Score Range
          </Text>
          <Box px={2}>
            <RangeSlider
              defaultValue={[30, 80]}
              min={0}
              max={100}
              step={5}
            >
              <RangeSliderTrack>
                <RangeSliderFilledTrack bg="brand.500" />
              </RangeSliderTrack>
              <RangeSliderThumb index={0} boxSize={6}>
                <Box color="brand.500" fontWeight="bold" fontSize="xs">
                  30
                </Box>
              </RangeSliderThumb>
              <RangeSliderThumb index={1} boxSize={6}>
                <Box color="brand.500" fontWeight="bold" fontSize="xs">
                  80
                </Box>
              </RangeSliderThumb>
            </RangeSlider>
            <Flex justify="space-between" mt={1}>
              <Text fontSize="xs" color="gray.500">0%</Text>
              <Text fontSize="xs" color="gray.500">100%</Text>
            </Flex>
          </Box>
        </Box>
        
        <Box flex="1" minW={{ base: "100%", md: "200px" }}>
          <Text fontSize="sm" fontWeight="medium" mb={2}>
            Date Range
          </Text>
          <Select size="sm" defaultValue="lastWeek">
            <option value="today">Today</option>
            <option value="yesterday">Yesterday</option>
            <option value="lastWeek">Last 7 days</option>
            <option value="lastMonth">Last 30 days</option>
            <option value="custom">Custom Range</option>
          </Select>
        </Box>
        
        <Box flex="1" minW={{ base: "100%", md: "200px" }}>
          <Text fontSize="sm" fontWeight="medium" mb={2}>
            Category
          </Text>
          <Select size="sm" defaultValue="all">
            <option value="all">All Categories</option>
            <option value="relevancy">Relevancy</option>
            <option value="precision">Context Precision</option>
            <option value="latency">Response Latency</option>
          </Select>
        </Box>
      </Flex>
      
      <Divider my={4} />
      
      <Flex 
        justify="space-between" 
        align={{ base: "stretch", md: "center" }}
        direction={{ base: "column", md: "row" }}
        wrap="wrap"
        gap={2}
      >
        <HStack spacing={2} wrap="wrap">
          <Text fontSize="sm" fontWeight="medium">
            Active Filters:
          </Text>
          <Badge colorScheme="brand" variant="solid" borderRadius="full" px={2}>
            Score: 30-80%
          </Badge>
          <Badge colorScheme="brand" variant="solid" borderRadius="full" px={2}>
            Last 7 days
          </Badge>
        </HStack>
        
        <Button size="xs" variant="ghost">
          Clear All Filters
        </Button>
      </Flex>
    </Box>
  );
};

export default EvaluationFilters;