"use client";

import { Input } from "@/components/ui/input";
import { LuSearch } from "react-icons/lu";

export default function SearchInput() {
  return (
    <div className="relative block">
      <LuSearch className="absolute h-4 w-4 top-2 left-4 text-muted-foreground" />
      <Input placeholder="Search" className="pl-10 bg-primary/10" />
    </div>
  );
}
