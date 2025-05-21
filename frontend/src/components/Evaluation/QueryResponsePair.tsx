import { 
  Box, 
  Flex, 
  Text, 
  Badge, 
  Accordion, 
  AccordionItem, 
  AccordionButton, 
  AccordionPanel, 
  AccordionIcon,
  HStack,
  useColorModeValue,
  Divider,
  Button
} from '@chakra-ui/react';
import { QueryResponsePair } from '../../types/evaluation';
import { format } from 'date-fns';

interface QueryResponsePairProps {
  pair: QueryResponsePair;
}

const QueryResponsePairComponent = ({ pair }: QueryResponsePairProps) => {
  // Calculate average score
  const averageScore = pair.metrics.reduce((sum, metric) => sum + metric.value, 0) / pair.metrics.length;
  
  // Determine score color
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'green';
    if (score >= 60) return 'yellow';
    return 'red';
  };
  
  const scoreColor = getScoreColor(averageScore);
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  
  return (
    <Box 
      borderWidth="1px" 
      borderRadius="lg" 
      bg={bgColor}
      mb={4}
      overflow="hidden"
    >
      <Flex 
        p={4} 
        borderBottomWidth="1px"
        borderColor={borderColor}
        justify="space-between"
        align="center"
      >
        <Box>
          <Text fontWeight="medium">
            Query #{pair.id}
          </Text>
          <Text fontSize="sm" color="gray.500">
            {format(new Date(pair.timestamp), 'PPp')}
          </Text>
        </Box>
        <HStack spacing={3}>
          <Badge 
            px={3} 
            py={1} 
            borderRadius="full" 
            colorScheme={scoreColor}
            fontSize="sm"
          >
            Score: {averageScore.toFixed(1)}%
          </Badge>
        </HStack>
      </Flex>
      
      <Box p={4}>
        <Text fontSize="sm" fontWeight="medium" color="gray.500" mb={1}>
          QUERY
        </Text>
        <Text p={3} bg="gray.50" borderRadius="md" fontFamily="mono" fontSize="sm" mb={4}>
          {pair.query}
        </Text>
        
        <Text fontSize="sm" fontWeight="medium" color="gray.500" mb={1}>
          RESPONSE
        </Text>
        <Text p={3} bg="gray.50" borderRadius="md" fontFamily="mono" fontSize="sm">
          {pair.response}
        </Text>
        
        {pair.groundTruth && (
          <>
            <Divider my={4} />
            <Accordion allowToggle>
              <AccordionItem border="none">
                <AccordionButton 
                  pl={0} 
                  _hover={{ bg: 'transparent' }}
                >
                  <Text fontSize="sm" fontWeight="medium" color="gray.500">
                    GROUND TRUTH
                  </Text>
                  <AccordionIcon />
                </AccordionButton>
                <AccordionPanel pb={4} pl={0}>
                  <Text p={3} bg="gray.50" borderRadius="md" fontFamily="mono" fontSize="sm">
                    {pair.groundTruth}
                  </Text>
                </AccordionPanel>
              </AccordionItem>
            </Accordion>
          </>
        )}
        
        <Divider my={4} />
        
        <Accordion allowToggle>
          <AccordionItem border="none">
            <AccordionButton 
              pl={0} 
              _hover={{ bg: 'transparent' }}
            >
              <Text fontSize="sm" fontWeight="medium" color="gray.500">
                METRICS
              </Text>
              <AccordionIcon />
            </AccordionButton>
            <AccordionPanel pb={4} pl={0}>
              <Box>
                {pair.metrics.map((metric) => (
                  <Flex 
                    key={metric.id} 
                    justify="space-between" 
                    align="center" 
                    mb={2}
                    p={2}
                    borderRadius="md"
                    bg="gray.50"
                  >
                    <Text fontSize="sm">
                      {metric.name}
                    </Text>
                    <Badge 
                      colorScheme={getScoreColor(metric.value)}
                    >
                      {metric.value}%
                    </Badge>
                  </Flex>
                ))}
              </Box>
            </AccordionPanel>
          </AccordionItem>
        </Accordion>
      </Box>
      
      <Flex 
        p={3} 
        borderTopWidth="1px"
        borderColor={borderColor}
        justify="flex-end"
        bg="gray.50"
      >
        <Button size="sm" variant="outline" colorScheme="brand">
          View Details
        </Button>
      </Flex>
    </Box>
  );
};

export default QueryResponsePairComponent;