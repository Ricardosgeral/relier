// server or client component depending on the parent

import { ExtendedUser } from "@/auth";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface UserInfoProps {
  user?: ExtendedUser;
  label: string;
}

export default function UserInfo({ user, label }: UserInfoProps) {
  return (
    <Card className="w-[600px] shadow-md">
      <CardHeader>
        <p className="text-md font-semibold text-center">{label}</p>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex flex-row items-center justify-between rounded-md border p-3 shadow-sm">
          <p className="text-sm font-medium">ID</p>
          <p className="truncate text-xs max-w-[185px] font-mono p-1 bg-slate-200 rounded-sm">
            {user?.id}
          </p>
        </div>
        <div className="flex flex-row items-center justify-between rounded-md border p-3 shadow-sm">
          <p className="text-sm font-medium">Name</p>
          <p className="truncate text-xs max-w-[185px] font-mono p-1 bg-slate-200 rounded-sm">
            {user?.name}
          </p>
        </div>
        <div className="flex flex-row items-center justify-between rounded-md border p-3 shadow-sm">
          <p className="text-sm font-medium">Email</p>
          <p className="truncate text-xs max-w-[185px] font-mono p-1 bg-slate-200 rounded-sm">
            {user?.email}
          </p>
        </div>
        <div className="flex flex-row items-center justify-between rounded-md border p-3 shadow-sm">
          <p className="text-sm font-medium">Role</p>
          <p className="truncate text-xs max-w-[185px] font-mono p-1 bg-slate-200 rounded-sm">
            {user?.role}
          </p>
        </div>
        <div className="flex flex-row items-center justify-between rounded-md border p-3 shadow-sm">
          <p className="text-sm font-medium">Two Factor Auth</p>
          <Badge variant={user?.isTwoFactorEnabled ? "success" : "destructive"}>
            {user?.isTwoFactorEnabled ? "ON" : "OFF"}
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
}
