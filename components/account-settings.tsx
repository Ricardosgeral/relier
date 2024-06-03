"use client";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useState, useTransition } from "react";
import { setSecurity } from "@/actions/set-security";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardContent } from "@/components/ui/card";

import {
  Select,
  SelectContent,
  SelectTrigger,
  SelectValue,
  SelectItem,
} from "@/components/ui/select";

import { Switch } from "@/components/ui/switch";

import { SettingsSchema, DeleteAccountSchema, NameSchema } from "@/schemas";
import {
  Form,
  FormField,
  FormControl,
  FormItem,
  FormLabel,
  FormDescription,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";

import { useCurrentUser } from "@/hooks/use-current-user";
import { FormSuccess } from "@/components/form-success";
import { FormError } from "@/components/form-error";
import { UserRole } from "@prisma/client";
import { deleteAccount } from "@/actions/delete-account";
import { Badge } from "@/components/ui/badge";
import { setName } from "@/actions/set-name";
import { UploadButton } from "@/app/utils/uploadthing";
import { useToast } from "@/components/ui/use-toast";
import Image from "next/image";
import { LuLoader2, LuTrash2 } from "react-icons/lu";
import { deleteProfilePhoto } from "@/actions/delete-profile-photo";
import { useRouter } from "next/navigation";
export default function AccountSettings() {
  const user = useCurrentUser();
  const router = useRouter();

  const [image, setImage] = useState(user?.image || "");

  const [imageIsDeleting, setimageIsDeleting] = useState(false);

  const [nameError, setNameError] = useState("");
  const [nameSuccess, setNameSuccess] = useState("");

  const [settingsError, setSettingsError] = useState("");
  const [settingsSuccess, setSettingsSuccess] = useState("");

  const [deleteError, setDeleteError] = useState("");
  const [deleteSuccess, setDeleteSuccess] = useState("");

  const [isPending, startTransition] = useTransition();

  const { toast } = useToast();

  const formName = useForm<z.infer<typeof NameSchema>>({
    resolver: zodResolver(NameSchema),
    defaultValues: {
      name: user?.name || "",
      image: user?.image || "",
      role: user?.role || "USER",
    },
  });

  const form = useForm<z.infer<typeof SettingsSchema>>({
    resolver: zodResolver(SettingsSchema),
    defaultValues: {
      email: user?.email || undefined,
      password: undefined,
      newPassword: undefined,
      isTwoFactorEnabled: user?.isTwoFactorEnabled || false,
    },
  });

  const formDelete = useForm<z.infer<typeof DeleteAccountSchema>>({
    resolver: zodResolver(DeleteAccountSchema),
    defaultValues: {
      delete: undefined,
    },
  });

  const onSubmitName = (values: z.infer<typeof NameSchema>) => {
    router.refresh();
    startTransition(() => {
      console.log(values.image);
      setName(values)
        .then((data) => {
          if (data.error) {
            setNameError(data.error);
          }
          if (data.success) {
            setNameSuccess(data.success);
          }
        })
        .catch(() => setNameError("Something went wrong"));
    });
  };

  const onSubmit = (values: z.infer<typeof SettingsSchema>) => {
    startTransition(() => {
      setSecurity(values)
        .then((data) => {
          if (data.error) {
            setSettingsError(data.error);
          }
          if (data.success) {
            setSettingsSuccess(data.success);
          }
        })
        .catch(() => setSettingsError("Something went wrong"));
    });
  };

  const onSubmitDeleteAccount = (
    values: z.infer<typeof DeleteAccountSchema>,
  ) => {
    startTransition(() => {
      deleteAccount(values)
        .then((data) => {
          if (data.errorDelete) {
            setDeleteError(data.errorDelete);
          }
          if (data.successDelete) {
            setDeleteSuccess(data.successDelete);
          }
        })
        .catch(() => setDeleteError("Something went wrong"));
    });
  };

  const handleImageDelete = (image: string) => {
    setimageIsDeleting(true);
    const imagekey = image.substring(image.lastIndexOf("/") + 1);
    fetch("/api/uploadthing/delete", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ imagekey }),
      cache: "no-store",
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          setImage("");
          deleteProfilePhoto(image);
          toast({ variant: "success", description: "Image removed" });
        }
      })
      .catch((error) => {
        toast({
          variant: "destructive",
          description: `Something went wrong: ${error}`,
        });
      })
      .finally(() => {
        setimageIsDeleting(false);
      });
  };

  return (
    <section className="flex h-full w-full flex-col gap-y-3">
      <Card className="p-2">
        <CardHeader>
          <p className="text-md text-center font-semibold">👷🏼‍♂️ Profile</p>
        </CardHeader>
        <CardContent className="flex items-center">
          <p className="pr-2 text-xs font-semibold">id</p>
          <Badge variant={"secondary"}>{user?.id?.toString()}</Badge>
        </CardContent>
        {user?.isOAuth && (
          <CardContent className="flex items-center">
            <p className="pr-2 text-xs font-semibold">email</p>
            <Badge variant={"secondary"}>{user?.email?.toString()}</Badge>
          </CardContent>
        )}
        <CardContent>
          <Form {...formName}>
            <form
              className="space-y-6"
              onSubmit={formName.handleSubmit(onSubmitName)}
            >
              <div className="space-y-4">
                {!user?.isOAuth && (
                  <FormField
                    control={formName.control}
                    name="image"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Profile image</FormLabel>
                        <FormControl>
                          <div className="flex w-full justify-center">
                            {image ? (
                              <div className="border-1 relative h-52 w-52">
                                <Image
                                  src={image}
                                  sizes="(max-width: 200px) 100vw, (max-width: 400px) 50vw, 33vw"
                                  alt="profile image"
                                  fill
                                  objectFit="cover"
                                  className="rounded-full border-2 object-cover"
                                />
                                <Button
                                  onClick={() => handleImageDelete(image)}
                                  type="button"
                                  size="icon"
                                  variant="outline"
                                  className="absolute bottom-0 left-[-10px] rounded-full"
                                >
                                  {imageIsDeleting ? (
                                    <LuLoader2 />
                                  ) : (
                                    <LuTrash2 className="text-red-500" />
                                  )}
                                </Button>
                              </div>
                            ) : (
                              <>
                                <div className="flex h-52 w-52 justify-center rounded-full border border-slate-200 pt-6">
                                  <UploadButton
                                    content={{
                                      button({ ready, isUploading }) {
                                        if (isUploading)
                                          return <div>Uploading...</div>;

                                        if (ready)
                                          return <div>Upload photo</div>;
                                      },
                                      allowedContent({ ready, isUploading }) {
                                        if (!ready)
                                          return "Checking what you allow";
                                        if (isUploading)
                                          return "Please wait...";
                                      },
                                    }}
                                    className="flex items-center ut-button:h-8 ut-button:bg-yellow-500 ut-button:text-sm ut-button:font-semibold ut-button:ring-1 ut-button:ring-yellow-500 after:ut-button:bg-yellow-200/50 after:ut-button:text-black ut-button:ut-readying:bg-yellow-500/50"
                                    endpoint="profilePhotoUploader"
                                    onClientUploadComplete={(res) => {
                                      const imageUrl = res[0].url;
                                      setImage(imageUrl);

                                      // Save the image URL to the server
                                      setName({
                                        ...formName.getValues(),
                                        image: imageUrl,
                                      })
                                        .then((data) => {
                                          if (data.error) {
                                            setNameError(data.error);
                                          } else {
                                            toast({
                                              variant: "success",
                                              description:
                                                "Image uploaded. Save it.",
                                            });
                                          }
                                        })
                                        .catch((error) => {
                                          toast({
                                            variant: "destructive",
                                            description: `Error! ${error.message}`,
                                          });
                                        });
                                    }}
                                    onUploadError={(error: Error) => {
                                      // Do something with the error.
                                      toast({
                                        variant: "destructive",
                                        description: `Error! ${error.message}`,
                                      });
                                    }}
                                  />
                                </div>
                              </>
                            )}
                          </div>
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                )}

                <FormField
                  control={formName.control}
                  name="name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Name</FormLabel>
                      <FormControl>
                        <Input
                          {...field}
                          placeholder="name"
                          disabled={isPending}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={formName.control}
                  name="role"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Role</FormLabel>
                      <Select
                        disabled={
                          user?.role?.toString() === "USER" ? true : isPending
                        }
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                      >
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Select a role" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value={UserRole.ADMIN}>Admin</SelectItem>
                          <SelectItem value={UserRole.USER}>User</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <Button type="submit" disabled={isPending}>
                Save
              </Button>
              <FormError message={nameError} />
              <FormSuccess message={nameSuccess} />
            </form>
          </Form>
        </CardContent>
      </Card>
      {!user?.isOAuth && (
        <Card className="p-2">
          <CardHeader>
            <p className="text-md text-center font-semibold">🔐 Security</p>
          </CardHeader>
          <CardContent>
            <Form {...form}>
              <form
                className="space-y-6"
                onSubmit={form.handleSubmit(onSubmit)}
              >
                <div className="space-y-4">
                  {user?.isOAuth === false && (
                    <>
                      <FormField
                        control={form.control}
                        name="email"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Email</FormLabel>
                            <FormControl>
                              <Input
                                {...field}
                                placeholder="email"
                                type="email"
                                disabled={isPending}
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <FormField
                        control={form.control}
                        name="password"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Password</FormLabel>
                            <FormControl>
                              <Input
                                {...field}
                                placeholder="password"
                                type="password"
                                disabled={isPending}
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <FormField
                        control={form.control}
                        name="newPassword"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>
                              New password | Confirm password{" "}
                            </FormLabel>
                            <FormControl>
                              <Input
                                {...field}
                                placeholder="new password"
                                type="password"
                                disabled={isPending}
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <FormField
                        control={form.control}
                        name="isTwoFactorEnabled"
                        render={({ field }) => (
                          <FormItem className="itens-center flex flex-row justify-between rounded-md shadow-sm">
                            <div className="space-y-0.5">
                              <FormLabel> Two Factor Authentication</FormLabel>
                              <FormDescription>
                                Enable two factor Authentication for your
                                account
                              </FormDescription>
                            </div>
                            <FormControl>
                              <Switch
                                disabled={isPending}
                                checked={field.value}
                                onCheckedChange={field.onChange}
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </>
                  )}
                </div>

                <Button type="submit" disabled={isPending}>
                  Save
                </Button>
                <FormError message={settingsError} />
                <FormSuccess message={settingsSuccess} />
              </form>
            </Form>
          </CardContent>
        </Card>
      )}
      <Card className="bg-red-100 p-2">
        <CardHeader>
          <p className="text-md text-center font-semibold dark:text-background/70">
            ⚡ Danger
          </p>
        </CardHeader>
        <CardContent className="">
          <Form {...formDelete}>
            <form
              className="space-y-6"
              onSubmit={formDelete.handleSubmit(onSubmitDeleteAccount)}
            >
              <div className="space-y-4">
                <FormField
                  control={formDelete.control}
                  name="delete"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>
                        <div className="space-y-2">
                          <h1 className="font-bold text-red-500">
                            Delete Account <span> 😟</span>
                          </h1>

                          <div className="flex flex-col space-y-4 dark:text-background/70">
                            <span>This action cannot be undone.</span>
                            <span className="text-sm font-normal">
                              To delete your account, write{" "}
                              <Badge
                                className="inline-flex dark:bg-red-200 dark:text-background/50"
                                variant="outline"
                              >
                                DELETE
                              </Badge>
                            </span>
                          </div>
                        </div>
                      </FormLabel>
                      <FormControl>
                        <Input
                          {...field}
                          placeholder="DELETE? Are you sure?"
                          disabled={isPending}
                          className="bg-white"
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <Button variant="destructive" type="submit" disabled={isPending}>
                Delete
              </Button>
              <FormError message={deleteError} />
              <FormSuccess message={deleteSuccess} />
            </form>
          </Form>
        </CardContent>
      </Card>
    </section>
  );
}
