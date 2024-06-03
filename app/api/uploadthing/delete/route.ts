import { currentUser } from "@/lib/auth";
import { NextResponse } from "next/server";
import { UTApi } from "uploadthing/server";

const utapi = new UTApi();

export async function POST(req: Request) {
  const user = await currentUser();

  if (!user?.id) return new NextResponse("Unauthorized use", { status: 401 });

  const { imagekey } = await req.json();

  try {
    const res = await utapi.deleteFiles(imagekey);
    return NextResponse.json(res);
  } catch (error) {
    console.log("error at uploading/delete", error);
    return new NextResponse("internal Server Error", { status: 500 });
  }
}
