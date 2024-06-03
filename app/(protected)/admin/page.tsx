"use client";

import { UserRole } from "@prisma/client";
import RoleGate from "@/components/auth/role-gate";
import { FormSuccess } from "@/components/form-success";
import { useCurrentRole } from "@/hooks/use-current-role";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { admin } from "@/actions/admin";

export default function AdminPage() {
  const role = useCurrentRole();

  async function onServerActionClick() {
    admin().then((data) => {
      if (data.error) {
        toast.error(data.error);
      }
      if (data.success) {
        toast.success(data.success);
      }
    });
  }

  async function onApiRouterClick() {
    fetch("/api/admin").then((response) => {
      if (response.ok) {
        toast.success("Allowed API Route");
      } else {
        toast.error("Forbidden API Route");
      }
    });
  }

  return (
    <Card className="w-[600px]">
      <CardHeader>
        <p className="text-md font-semibold text-center">🔑 Admin</p>
      </CardHeader>
      <CardContent className="space-y-2">
        <RoleGate allowedRole={UserRole.ADMIN}>
          <FormSuccess message="You are Admin"></FormSuccess>
        </RoleGate>
        <div className="flex flex-row items-center justify-between rounded-sm border p-3 shadow-sm">
          <p className="text-sm font-medium">Admin-only API Route</p>
          <Button onClick={onApiRouterClick}>Click to test</Button>
        </div>
        <div className="flex flex-row items-center justify-between rounded-sm border p-3 shadow-sm">
          <p className="text-sm font-medium">Admin-only Server Action</p>
          <Button onClick={onServerActionClick}>Click to test</Button>
        </div>
      </CardContent>
      <CardFooter>Current role: {role}</CardFooter>
    </Card>
  );
}
