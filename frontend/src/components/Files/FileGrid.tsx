import { useState } from 'react';
import { 
  SimpleGrid, 
  Box, 
  Text, 
  Input, 
  InputGroup, 
  InputLeftElement,
  Flex,
  Select,
  HStack,
  Button,
  useBreakpointValue
} from '@chakra-ui/react';
import { Search, SortAsc } from 'lucide-react';
import { FileData } from '../../types/file';
import FileCard from './FileCard';

interface FileGridProps {
  files: FileData[];
  onDelete: (fileId: string) => void;
}

type SortOption = 'name-asc' | 'name-desc' | 'date-asc' | 'date-desc' | 'size-asc' | 'size-desc';

const FileGrid = ({ files, onDelete }: FileGridProps) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [sortOption, setSortOption] = useState<SortOption>('date-desc');
  const [viewType, setViewType] = useState<'grid' | 'list'>('grid');
  
  const columns = useBreakpointValue({ base: 1, sm: 2, md: 3, lg: 4 }) || 1;
  
  const filteredFiles = files.filter(file => 
    file.name.toLowerCase().includes(searchQuery.toLowerCase())
  );
  
  const sortedFiles = [...filteredFiles].sort((a, b) => {
    switch (sortOption) {
      case 'name-asc':
        return a.name.localeCompare(b.name);
      case 'name-desc':
        return b.name.localeCompare(a.name);
      case 'date-asc':
        return new Date(a.uploadDate).getTime() - new Date(b.uploadDate).getTime();
      case 'date-desc':
        return new Date(b.uploadDate).getTime() - new Date(a.uploadDate).getTime();
      case 'size-asc':
        return a.size - b.size;
      case 'size-desc':
        return b.size - a.size;
      default:
        return 0;
    }
  });

  return (
    <Box>
      <Flex 
        direction={{ base: 'column', md: 'row' }} 
        justify="space-between"
        align={{ base: 'stretch', md: 'center' }}
        mb={6}
        gap={4}
      >
        <InputGroup maxW={{ base: '100%', md: '300px' }}>
          <InputLeftElement pointerEvents="none">
            <Search size={18} color="gray.300" />
          </InputLeftElement>
          <Input
            placeholder="Search files..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </InputGroup>
        
        <HStack spacing={4}>
          <Select 
            value={sortOption} 
            onChange={(e) => setSortOption(e.target.value as SortOption)}
            maxW="200px"
            size="md"
          >
            <option value="date-desc">Newest first</option>
            <option value="date-asc">Oldest first</option>
            <option value="name-asc">Name (A-Z)</option>
            <option value="name-desc">Name (Z-A)</option>
            <option value="size-desc">Size (Large-Small)</option>
            <option value="size-asc">Size (Small-Large)</option>
          </Select>
          
          <HStack>
            <Button
              size="sm"
              variant={viewType === 'grid' ? 'solid' : 'outline'}
              colorScheme={viewType === 'grid' ? 'brand' : 'gray'}
              onClick={() => setViewType('grid')}
            >
              Grid
            </Button>
            <Button
              size="sm"
              variant={viewType === 'list' ? 'solid' : 'outline'}
              colorScheme={viewType === 'list' ? 'brand' : 'gray'}
              onClick={() => setViewType('list')}
            >
              List
            </Button>
          </HStack>
        </HStack>
      </Flex>
      
      {sortedFiles.length === 0 ? (
        <Box textAlign="center" py={8}>
          <Text color="gray.500">No files found</Text>
        </Box>
      ) : viewType === 'grid' ? (
        <SimpleGrid columns={columns} spacing={6}>
          {sortedFiles.map((file) => (
            <FileCard 
              key={file.id} 
              file={file} 
              onDelete={onDelete}
              viewType={viewType}
            />
          ))}
        </SimpleGrid>
      ) : (
        <Box>
          {sortedFiles.map((file) => (
            <Box key={file.id} mb={3}>
              <FileCard 
                file={file} 
                onDelete={onDelete}
                viewType={viewType}
              />
            </Box>
          ))}
        </Box>
      )}
    </Box>
  );
};

export default FileGrid;