"use client";

import { useState } from 'react';
import Link from 'next/link';
import { Search } from 'lucide-react';

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import { Badge } from "@/components/ui/badge";



export default async function Page() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDepartment, setSelectedDepartment] = useState('');

  const departments = [
    'Computer Science',
    'English',
    'Biology',
    'Chemistry',
    'Mathematics',
    'Physics',
    'Psychology',
    'Business',
    'Engineering',
    'History',
    'Political Science',
    'Sociology',
    'Art & Art History',
    'Music',
  ];

  const recentUploads = [
    { id: 'chem-1110', code: 'CHEM:1110', name: 'Principles of Chemistry I', department: 'Chemistry', lastUpdated: '2025-04-15' },
    { id: 'hist-1010', code: 'HIST:1010', name: 'Issues in Human History', department: 'History', lastUpdated: '2025-04-14' },
    { id: 'psych-1001', code: 'PSY:1001', name: 'Elementary Psychology', department: 'Psychology', lastUpdated: '2025-04-13' },
    { id: 'phil-1033', code: 'PHIL:1033', name: 'Philosophy and Human Nature', department: 'Philosophy', lastUpdated: '2025-04-12' },
  ];

  const featuredCourses = [
    { id: 'cs-1110', code: 'CS:1110', name: 'Introduction to Computer Science', department: 'Computer Science', lastUpdated: '2025-04-01' },
    { id: 'math-1850', code: 'MATH:1850', name: 'Calculus I', department: 'Mathematics', lastUpdated: '2025-03-15' },
    { id: 'engl-1200', code: 'ENGL:1200', name: 'Creative Writing', department: 'English', lastUpdated: '2025-03-28' },
    { id: 'biol-1411', code: 'BIOL:1411', name: 'Foundations of Biology', department: 'Biology', lastUpdated: '2025-04-12' },
  ];


  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-black text-white">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="bg-yellow-400 h-10 w-10 rounded-full flex items-center justify-center">
              <span className="text-black font-bold text-xl">UI</span>
            </div>
            <h1 className="text-2xl font-bold">UISyllabi</h1>
          </div>
          
          <NavigationMenu>
            <NavigationMenuList>
              <NavigationMenuItem>
                <Link href="/" legacyBehavior passHref>
                  <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                    Home
                  </NavigationMenuLink>
                </Link>
              </NavigationMenuItem>
              <NavigationMenuItem>
                <NavigationMenuTrigger>Departments</NavigationMenuTrigger>
                <NavigationMenuContent>
                  <div className="grid grid-cols-2 gap-3 p-4 w-96">
                    {departments.slice(0, 8).map((dept) => (
                      <Link key={dept} href={`/departments/${dept.toLowerCase().replace(/\s+/g, '-')}`} legacyBehavior passHref>
                        <NavigationMenuLink className="block p-2 hover:bg-gray-100 rounded">
                          {dept}
                        </NavigationMenuLink>
                      </Link>
                    ))}
                    <Link href="/departments" legacyBehavior passHref>
                      <NavigationMenuLink className="col-span-2 text-center block p-2 text-blue-600 hover:underline">
                        View All Departments →
                      </NavigationMenuLink>
                    </Link>
                  </div>
                </NavigationMenuContent>
              </NavigationMenuItem>
              <NavigationMenuItem>
                <Link href="/upload" legacyBehavior passHref>
                  <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                    Upload Syllabus
                  </NavigationMenuLink>
                </Link>
              </NavigationMenuItem>
              <NavigationMenuItem>
                <Link href="/about" legacyBehavior passHref>
                  <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                    About
                  </NavigationMenuLink>
                </Link>
              </NavigationMenuItem>
            </NavigationMenuList>
          </NavigationMenu>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-yellow-400 py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-4">Find Your Course Syllabus</h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Access syllabuses for University of Iowa courses in one convenient location.
            Plan your semester with confidence.
          </p>
          
          <div className="max-w-xl mx-auto flex gap-2">
            <div className="relative flex-grow">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-500" />
              <Input
                type="text"
                placeholder="Search by course name or code..."
                className="pl-10 bg-white"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <Button variant="default" className="bg-black hover:bg-gray-800">
              Search
            </Button>
          </div>
        </div>
      </section>

      {/* Main Content Area */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <Tabs defaultValue="featured" className="w-full">
            <TabsList className="grid w-full max-w-md mx-auto mb-8 grid-cols-3">
              <TabsTrigger value="featured">Featured</TabsTrigger>
              <TabsTrigger value="recent">Recent Uploads</TabsTrigger>
              <TabsTrigger value="departments">Departments</TabsTrigger>
            </TabsList>
            
            {/* Featured Courses Tab */}
            <TabsContent value="featured">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {featuredCourses.map((course) => (
                  <Card key={course.id} className="overflow-hidden">
                    <CardHeader className="pb-2">
                      <Badge variant="outline" className="mb-2 text-xs w-fit">{course.department}</Badge>
                      <CardTitle className="text-lg">{course.name}</CardTitle>
                    </CardHeader>
                    <CardContent className="pb-2">
                      <p className="text-gray-600">{course.code}</p>
                      <p className="text-xs text-gray-500 mt-2">Updated: {course.lastUpdated}</p>
                    </CardContent>
                    <CardFooter>
                      <Button variant="link" asChild className="p-0">
                        <Link href={`/course/${course.id}`}>View Syllabus</Link>
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
              </div>
            </TabsContent>
            
            {/* Recent Uploads Tab */}
            <TabsContent value="recent">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {recentUploads.map((course) => (
                  <Card key={course.id} className="overflow-hidden">
                    <CardHeader className="pb-2">
                      <Badge variant="outline" className="mb-2 text-xs w-fit">{course.department}</Badge>
                      <CardTitle className="text-lg">{course.name}</CardTitle>
                    </CardHeader>
                    <CardContent className="pb-2">
                      <p className="text-gray-600">{course.code}</p>
                      <p className="text-xs text-gray-500 mt-2">Updated: {course.lastUpdated}</p>
                    </CardContent>
                    <CardFooter>
                      <Button variant="link" asChild className="p-0">
                        <Link href={`/course/${course.id}`}>View Syllabus</Link>
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
              </div>
            </TabsContent>
            
            {/* Departments Tab */}
            <TabsContent value="departments">
              <div className="max-w-sm mx-auto mb-8">
                <Select onValueChange={setSelectedDepartment} value={selectedDepartment}>
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Select a department" />
                  </SelectTrigger>
                  <SelectContent>
                    {departments.map((dept) => (
                      <SelectItem key={dept} value={dept}>
                        {dept}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {departments.map((dept) => (
                  <Link 
                    key={dept} 
                    href={`/departments/${dept.toLowerCase().replace(/\s+/g, '-')}`} 
                    className="block"
                  >
                    <Card 
                      className={`transition cursor-pointer hover:border-yellow-400 ${
                        selectedDepartment === dept ? 'border-yellow-400 bg-yellow-50' : ''
                      }`}
                    >
                      <CardContent className="p-4 text-center">
                        {dept}
                      </CardContent>
                    </Card>
                  </Link>
                ))}
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-black text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h3 className="text-2xl font-bold mb-4">Have a syllabus to share?</h3>
          <p className="mb-8 max-w-2xl mx-auto">
            Help your fellow Hawkeyes by uploading course syllabuses. Together we can build a comprehensive resource for the UI community.
          </p>
          <Button className="bg-yellow-400 hover:bg-yellow-500 text-black" asChild>
            <Link href="/upload">Upload Syllabus</Link>
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-300 py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between">
            <div className="mb-6 md:mb-0">
              <div className="flex items-center gap-3 mb-4">
                <div className="bg-yellow-400 h-8 w-8 rounded-full flex items-center justify-center">
                  <span className="text-black font-bold text-sm">UI</span>
                </div>
                <h2 className="text-xl font-bold text-white">UISyllabi</h2>
              </div>
              <p className="max-w-md">
                A student-driven initiative to make University of Iowa course materials more accessible.
              </p>
            </div>
            
            <div className="grid grid-cols-2 gap-8">
              <div>
                <h4 className="font-semibold text-white mb-4">Navigation</h4>
                <ul className="space-y-2">
                  <li><Link href="/" className="hover:text-yellow-400">Home</Link></li>
                  <li><Link href="/departments" className="hover:text-yellow-400">Departments</Link></li>
                  <li><Link href="/upload" className="hover:text-yellow-400">Upload</Link></li>
                  <li><Link href="/about" className="hover:text-yellow-400">About Us</Link></li>
                </ul>
              </div>
              
              <div>
                <h4 className="font-semibold text-white mb-4">Contact</h4>
                <ul className="space-y-2">
                  <li>uisyllabi@uiowa.edu</li>
                  <li>Iowa City, IA</li>
                </ul>
              </div>
            </div>
          </div>
          
          <div className="border-t border-gray-700 mt-8 pt-8 text-center">
            <p>© {new Date().getFullYear()} UISyllabi. Not an official University of Iowa website.</p>
          </div>
        </div>
      </footer>
    </main>
  );
}